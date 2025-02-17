output "event_store" {
  description = "The full ID of the BigQuery table acting as the Octue Twined services event store."
  value       = module.octue_twined.event_store
}


output "service_registry" {
  description = "The URL of the service registry."
  value       = module.octue_twined.service_registry
}


output "services_topic" {
  description = "The Pub/Sub topic that all Octue Twined service events are published to."
  value       = module.octue_twined.services_topic
}
