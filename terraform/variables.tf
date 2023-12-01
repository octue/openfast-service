variable "project" {
  type    = string
  default = "octue-openfast"
}

variable "project_number" {
  type = string
  default = "86611255144"
}

variable "region" {
  type = string
  default = "europe-west3"
}

variable "github_organisation" {
  type    = string
  default = "octue"
}

variable "credentials_file" {
  type    = string
  default = "gcp-credentials.json"
}

variable "service_namespace" {
  type    = string
  default = "octue"
}

variable "service_name" {
  type    = string
  default = "openfast-service"
}

variable "environment" {
  type    = string
  default = "main"
}
