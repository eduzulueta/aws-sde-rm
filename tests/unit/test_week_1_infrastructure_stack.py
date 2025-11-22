import aws_cdk as core
import aws_cdk.assertions as assertions

from week_1_infrastructure.week_1_infrastructure_stack import Week1InfrastructureStack

# example tests. To run these tests, uncomment this file along with the example
# resource in week_1_infrastructure/week_1_infrastructure_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Week1InfrastructureStack(app, "week-1-infrastructure")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
