terraform {
  required_version = ">= 1.8.0, <2"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>6.12"
    }
  }

  cloud {
    organization = "octue"
    workspaces {
      project = "octue-openfast"
      tags = ["openfast-service"]
    }
  }
}


provider "google" {
  project     = var.google_cloud_project_id
  region      = var.google_cloud_region
}


data "google_client_config" "default" {}


module "octue_twined_static" {
  source = "git::github.com/octue/terraform-octue-twined-static.git?ref=create-initial-module"
  google_cloud_project_id = var.google_cloud_project_id
  google_cloud_region = var.google_cloud_region
  github_organisation = var.github_organisation
}
