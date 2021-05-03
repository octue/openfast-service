import os

from octue.cloud.pub_sub.service import Service
from octue.resources.service_backends import GCPPubSubBackend


def test_deployment():
    """Test that the Google Cloud Run integration works, providing a service that can be asked questions and send
    responses.
    """
    service_id = "octue.services.8765b5f2-1778-4a6f-809d-46b91e01bd97"
    asker = Service(backend=GCPPubSubBackend(project_name=os.environ["TEST_PROJECT_NAME"]))

    input_values = {
        "alpha_range": [-10, 10, 5],
        "inflow_speed": 1,
        "kinematic_viscosity": 1e-6,
        "characteristic_length": 1e-6,
        "mach_number": 0,
        "n_critical": 9,
        "re_xtr": [5e5, 5e5]
    }

    subscription, _ = asker.ask(service_id=service_id, input_values=input_values)
    answer = asker.wait_for_answer(subscription, timeout=1000)
    assert all(key in answer["output_values"] for key in ("cl", "cd", "cm"))


if __name__ == "__main__":
    test_deployment()
