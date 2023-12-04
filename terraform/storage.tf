resource "google_storage_bucket" "openfast_service_crash_diagnostics" {
  name                        = "${var.service_namespace}-${var.openfast_service_name}"
  location                    = "EU"
  force_destroy               = true
  uniform_bucket_level_access = true
}


resource "google_storage_bucket" "turbsim_service_crash_diagnostics" {
  name                        = "${var.service_namespace}-${var.turbsim_service_name}"
  location                    = "EU"
  force_destroy               = true
  uniform_bucket_level_access = true
}


resource "google_storage_bucket" "output_data" {
  name                        = "${var.project}-data"
  location                    = "EU"
  force_destroy               = true
  uniform_bucket_level_access = true
}


resource "google_storage_bucket" "test_data" {
  name                        = "${var.project}-test-data"
  location                    = "EU"
  force_destroy               = true
  uniform_bucket_level_access = true
}
