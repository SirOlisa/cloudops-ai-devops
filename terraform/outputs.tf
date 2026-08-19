output "ecr_repository_url" {
  value       = aws_ecr_repository.app_repo.repository_url
  description = "The URL of the ECR repository to push Docker images"
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.main.name
  description = "The name of the created ECS Cluster"
}

output "vpc_id" {
  value       = aws_vpc.main.id
  description = "The main VPC Identifier"
}

output "ecs_service_name" {
  value       = aws_ecs_service.main.name
  description = "The name of the created ECS Service"
}