import json
import sys
import applications.app_base

def tf_batch_service(mem_limit, image):
    """
    :type mem_limit: int
    :type image: str
    :rtype: dict
    """
    service = {
        'name': "tensorflow",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": mem_limit},
        'ports': [
            {
                'name': "Tensorboard web interface",
                'protocol': "http",
                'port_number': 6006,
                'path': "/",
                'is_main_endpoint': False,
		'expose': True
            }
        ],
        'networks': [],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    return service

APP_NAME = 'tensorflow'

def gen_app(mem_limit, tf_image):
    services = [tf_batch_service(mem_limit, tf_image)]
    return applications.app_base.fill_app_template(APP_NAME, False, services)

DOCKER_REGISTRY = 'docker-registry:5000/'

options = [
    ('mem_limit', 16 * (1024**3), 'Tensorflow memory limit (bytes)'),
    ('tf_image', DOCKER_REGISTRY + 'zapps/tensorflow', 'Tensorflow image'),
]

if __name__ == "__main__":
    args = {}
    for opt in options:
        args[opt[0]] = opt[1]
    app_dict = gen_app(**args)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')

