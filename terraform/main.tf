terraform {
  required_version = ">= 1.9, < 2.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.35"
    }
  }
}

provider "kubernetes" {
  config_path    = pathexpand("~/.kube/config")
  config_context = "kind-health-monitor"
}

variable "image" {
  type    = string
  default = "service-health-monitor:local"
}

resource "kubernetes_namespace_v1" "lab" {
  metadata {
    name = "health-monitor"
  }
}

resource "kubernetes_deployment_v1" "target" {
  metadata {
    name      = "target"
    namespace = kubernetes_namespace_v1.lab.metadata[0].name
  }
  spec {
    replicas = 1
    selector {
      match_labels = { app = "target" }
    }
    template {
      metadata {
        labels = { app = "target" }
      }
      spec {
        container {
          name              = "target"
          image             = var.image
          image_pull_policy = "IfNotPresent"
          command           = ["python", "-m", "app.target"]
          port {
            container_port = 8000
          }
          readiness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            period_seconds = 5
          }
          liveness_probe {
            http_get {
              path = "/live"
              port = 8000
            }
            period_seconds = 5
          }
          resources {
            requests = { cpu = "50m", memory = "32Mi" }
            limits   = { cpu = "250m", memory = "128Mi" }
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "target" {
  metadata {
    name      = "target"
    namespace = kubernetes_namespace_v1.lab.metadata[0].name
  }
  spec {
    selector = { app = "target" }
    port {
      port        = 8000
      target_port = 8000
    }
  }
}

resource "kubernetes_deployment_v1" "monitor" {
  metadata {
    name      = "monitor"
    namespace = kubernetes_namespace_v1.lab.metadata[0].name
  }
  spec {
    replicas = 1
    selector {
      match_labels = { app = "monitor" }
    }
    template {
      metadata {
        labels = { app = "monitor" }
      }
      spec {
        container {
          name              = "monitor"
          image             = var.image
          image_pull_policy = "IfNotPresent"
          env {
            name  = "TARGET_URL"
            value = "http://${kubernetes_service_v1.target.metadata[0].name}:8000/health"
          }
          resources {
            requests = { cpu = "25m", memory = "32Mi" }
            limits   = { cpu = "100m", memory = "128Mi" }
          }
        }
      }
    }
  }
}
