terraform {
  required_providers {
    # https://registry.terraform.io/providers/kreuzwerker/docker/latest/docs
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.6.2"
    }
  }
}

variable "TELEGRAM_API_ID" {
  type = string
  sensitive   = true
}

variable "TELEGRAM_API_HASH" {
  type = string
  sensitive   = true
}

variable "TELEGRAM_API_PHONE_NUMBER" {
  type = string
  sensitive   = true
}

variable    "TELEGRAM_SESSION_AUTH_KEY" {
  type = string
  sensitive   = true
}

variable    "TELEGRAM_SESSION_DC_ID" {
  type = string
}

variable    "TELEGRAM_SESSION_SERVER_ADDRESS" {
  type = string
}

variable "docker_host_uri" {
  type = string
}

variable "docker_image" {
  type = string
}

variable "deploy_domain" {
  type = string
}

variable "docker_container_name" {
  type = string
}

variable "ghcr_username" {
  type = string
  sensitive   = true
}

variable "ghcr_token" {
  type = string
  sensitive   = true
}

variable "certresolver" {
  type        = string
  default     = "letsEncrypt"
  description = "The id of the certificate resolver to use."
}

provider "docker" {
  host = var.docker_host_uri
  ssh_opts = [
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null"
  ]
  registry_auth {
    address  = "ghcr.io"
    username = var.ghcr_username
    password = var.ghcr_token
  }
}

# Create Docker image
resource "docker_image" "telega" {
  name = var.docker_image
}

# Create Docker container using the telega image
resource "docker_container" "telega" {
  image             = docker_image.telega.image_id
  name              = var.docker_container_name
  must_run          = true
  publish_all_ports = true
  restart           = "always"
  env = [
    "TELEGRAM_API_ID=${var.TELEGRAM_API_ID}",
    "TELEGRAM_API_HASH=${var.TELEGRAM_API_HASH}",
    "TELEGRAM_API_PHONE_NUMBER=${var.TELEGRAM_API_PHONE_NUMBER}",
    "TELEGRAM_SESSION_AUTH_KEY=${var.TELEGRAM_SESSION_AUTH_KEY}",
    "TELEGRAM_SESSION_DC_ID=${var.TELEGRAM_SESSION_DC_ID}",
    "TELEGRAM_SESSION_SERVER_ADDRESS=${var.TELEGRAM_SESSION_SERVER_ADDRESS}"
  ]

  labels {
    label = "traefik.http.routers.${var.docker_container_name}.rule"
    value = "Host(`${var.deploy_domain}`)"
  }
  labels {
    label = "traefik.http.routers.${var.docker_container_name}.tls"
    value = true
  }
  labels {
    label = "traefik.http.routers.${var.docker_container_name}.tls.certresolver"
    value = var.certresolver
  }
}
