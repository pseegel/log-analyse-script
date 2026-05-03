resource "aws_cloudwatch_log_group" "ecs_task" {
  name              = "/ecs/log-analyse-task"
  retention_in_days = 7
}
