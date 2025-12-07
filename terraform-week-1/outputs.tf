output "s3_bucket_name" {
  value = aws_s3_bucket.data_bucket.id
}

output "kinesis_stream_name" {
  value = aws_kinesis_stream.data_stream.name
}

output "kms_key_arn" {
  value = aws_kms_key.data_key.arn
}