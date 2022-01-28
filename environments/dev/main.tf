# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


locals {
  env = "dev"
}

provider "google" {
  project = var.project
}

# module "vpc" {
#   source  = "../../modules/vpc"
#   project = "${var.project}"
#   env     = "${local.env}"
# }

# module "http_server" {
#   source  = "../../modules/http_server"
#   project = "${var.project}"
#   subnet  = "${module.vpc.subnet}"
# }

# module "firewall" {
#   source  = "../../modules/firewall"
#   project = "${var.project}"
#   subnet  = "${module.vpc.subnet}"
# }

data "google_client_config" "current" {
}

module "data_fusion" {
  source  = "terraform-google-modules/data-fusion/google"
  version = "1.1.0"

  name    = "df-instance-01-terraform-ha"
  project = var.project
  region  = var.region
  data_fusion_service_account = "bichapter@appspot.gserviceaccount.com"
  type    = "BASIC"
  network = "data-fusion-vpc-terraform-ha"
  # options = {
  #    "accelerators.accelerator_type":"CDC"
  #    "accelerators.state":"ENABLED"
  # }
  
}

resource "null_resource" "df-enable-replication-mode" {
  provisioner "local-exec" {
      command = "python3 ${path.module}/df-enable-replication.py -p ${var.project} -l ${var.region} -i df-instance-01-terraform-ha -t ${data.google_client_config.current.access_token}"
  }

  depends_on = [module.data_fusion.instance]
}
