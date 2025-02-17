variable "google_cloud_project_id" {
  type    = string
  default = "octue-openfast"
}


variable "google_cloud_region" {
  type = string
  default = "europe-west3"
}


variable "github_organisation" {
  type    = string
  default = "octue"
}


variable "service_account_names" {
  type = set(string)
  default = ["cortadocodes", "thclark"]
}


variable "deletion_protection" {
  type    = bool
  default = false
}


variable "cluster_queue" {
  type = object(
    {
      name                 = string
      max_cpus              = number
      max_memory            = string
      max_ephemeral_storage = string
    }
  )
  default = {
    name                  = "cluster-queue"
    max_cpus              = 100
    max_memory            = "256Gi"
    max_ephemeral_storage = "256Gi"
  }
}
