variable environment {}
variable region {}
variable function_name {}
variable role {}
variable env_vars {
  default = null
}
variable timeout {
  default = 300
}
variable memory_size {
  default = 512
}
variable architectures {
  default = ["arm64"]
}
variable platform {
  default = "linux/arm64"
}
variable ephemeral_storage {
  default = null
}