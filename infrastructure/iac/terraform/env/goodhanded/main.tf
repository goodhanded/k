
module "s3_bucket" {
  source = "../../modules/resources/aws/s3/s3_bucket"
  bucket = "goodhanded-voice-transcription"
}