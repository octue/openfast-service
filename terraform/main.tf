terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.53.1"
    }
  }
  cloud {
    organization = "octue"
    workspaces {
      name = "octue-openfast"
    }
  }
}


resource "google_project_service" "pub_sub" {
  project = var.project
  service = "pubsub.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }
}


resource "google_project_service" "cloud_resource_manager" {
  project = var.project
  service = "cloudresourcemanager.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }
}


resource "google_project_service" "iam" {
  project = var.project
  service = "iam.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }
}


resource "google_project_service" "artifact_registry" {
  project = var.project
  service = "artifactregistry.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }
}


resource "google_project_service" "cloud_run" {
  project = var.project
  service = "run.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }
}


resource "google_project_service" "secret_manager" {
  project = var.project
  service = "secretmanager.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }
}

#
#resource "google_project_service" "cloud_build" {
#  project = var.project
#  service = "cloudbuild.googleapis.com"
#
#  timeouts {
#    create = "30m"
#    update = "40m"
#  }
#}


provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
}
