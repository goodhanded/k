variable environment {}
variable job_name {}
variable role_arn {}
variable glue_version { default = "4.0" }
variable execution_class { default = "STANDARD" }
variable num_workers { default = 2 }
variable worker_type { default = "G.1X" }
variable timeout { default = 5 }
variable command_name { default = "glueetl" }
variable script_location {}
variable default_arguments { default = [] }
variable max_concurrent_runs { default = 1 }