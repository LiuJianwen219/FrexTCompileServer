import os
import sys

sys.path.append('/FrexT/k8s_handler')  # 导入test文件的绝对路径

from kubernetes import client, config
import uuid
from time import sleep
from k8s_handler import constants as const
from compiler import constants as c_const
from compiler import constants as c_const
import config as cfg


class k8s_handler:
    def __init__(self):
        # Configs can be set in Configuration class directly or using helper
        # utility. If no argument provided, the config will be loaded from
        # default location.
        config.load_incluster_config()
        self.api_instance = client.BatchV1Api()
        self.jobName = None
        self.namespace = "default"

    # Create a job object with client-python API. The job we
    # created is same as the `pi-job.yaml` in the /examples folder.
    # "mod60", "topMod60"
    def create_job_object(self, values):
        # volumes mount to pod
        volume_mount_vivado = client.V1VolumeMount(
            name="vivado",
            mount_path=const.vivadoPath,
        )

        # volume definitions
        volume_vivado = client.V1Volume(
            name="vivado",
            host_path=client.V1HostPathVolumeSource(
                path=const.vivadoPath,
                type="Directory",
            )
        )

        # Configureate Pod template container
        container = client.V1Container(
            name="cmp-job-" + uuid.uuid1().__str__(),
            image=const.image,
            command=["python"],
            args=[
                "main.py",
                "-u"+values[c_const.c_userId],
                "-t"+values[c_const.c_testId],
                "-s"+values[c_const.c_submitId],
                "-c"+values[c_const.c_topic],
                "-n"+values[c_const.c_topModuleName],
                "-l"+values[c_const.c_tclName],
                "-f"+values[c_const.c_fileServerUrl]
            ],
            volume_mounts=[
                volume_mount_vivado,
            ],
        )

        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(),
            spec=client.V1PodSpec(
                restart_policy="Never",
                containers=[container],
                volumes=[
                    volume_vivado,
                ],
            ),
        )

        # Create the specification of deployment
        spec = client.V1JobSpec(
            template=template,
            backoff_limit=4,
            ttl_seconds_after_finished=const.ttl_seconds_after_finished,
        )

        # Instantiate the job object
        self.jobName = "cmp-job-" + uuid.uuid1().__str__()
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(
                name=self.jobName
            ),
            spec=spec,
        )

        return job

    def create_job(self, job):
        api_response = self.api_instance.create_namespaced_job(
            body=job,
            namespace=self.namespace,
        )
        print("Job created. status='%s'" % str(api_response.status))
        # Job created. status='{'active': None,
        #  'completion_time': None,
        #  'conditions': None,
        #  'failed': None,
        #  'start_time': None,
        #  'succeeded': None}'
        # get_job_status(api_instance)

    def get_job_status(self):
        job_completed = False
        while not job_completed:
            api_response = self.api_instance.read_namespaced_job_status(
                name=self.jobName,
                namespace=self.namespace)
            if api_response.status.succeeded is not None or \
                    api_response.status.failed is not None:
                job_completed = True
            sleep(1)
            print("Job status='%s'" % str(api_response.status))

    # def update_job(self, job):
    #     # Update container image
    #     job.spec.template.spec.containers[0].image = "perl"
    #     api_response = self.api_instance.patch_namespaced_job(
    #         name=self.jobName,
    #         namespace=self.namespace,
    #         body=job)
    #     print("Job updated. status='%s'" % str(api_response.status))

    # def delete_job(self):
    #     api_response = self.api_instance.delete_namespaced_job(
    #         name=self.jobName,
    #         namespace=self.namespace,
    #         body=client.V1DeleteOptions(
    #             propagation_policy='Foreground',
    #             grace_period_seconds=5))
    #     print("Job deleted. status='%s'" % str(api_response.status))


def list_pods(namespace):
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs in namespace: " + namespace + ":")
    # ret = v1.list_pod_for_all_namespaces(watch=False)
    ret = v1.list_namespaced_pod(namespace=namespace)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def test():
    job_handler = k8s_handler()
    job_spec = job_handler.create_job_object("/tmp/FrexT", "test", "topMod60")
    job_handler.create_job(job_spec)


if __name__ == '__main__':
    list_pods("default")
    test()
