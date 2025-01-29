terraform {
  backend "s3" {
    bucket = "goodhanded-infrastructure"
    key    = "env/goodhanded/terraform.tfstate"
    region = "us-east-1"
  }
}
