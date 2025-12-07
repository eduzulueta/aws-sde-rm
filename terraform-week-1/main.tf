# --- 1. KMS Key (Data Sovereignty) ---
resource "aws_kms_key" "data_key" {
  description             = "KMS Key for Data Engineering Lab Week 1"
  enable_key_rotation     = true
  deletion_window_in_days = 7
}

# --- 2. S3 Bucket (Data Lake Landing Zone) ---
resource "aws_s3_bucket" "data_bucket" {
  # Terraform requires unique bucket names. We use a prefix + random string logic usually,
  # but here we rely on Terraform to generate a unique suffix if we don't specify the full name,
  # or we just use a very specific name.
  bucket_prefix = "week-1-tf-lake-"

  # Lab Safety: Allows deleting the bucket even if it contains objects
  force_destroy = true
}

# Enable Versioning
resource "aws_s3_bucket_versioning" "data_bucket_ver" {
  bucket = aws_s3_bucket.data_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable KMS Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "data_bucket_enc" {
  bucket = aws_s3_bucket.data_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data_key.arn
    }
  }
}

# --- 3. Kinesis Data Stream (The Pipe) ---
resource "aws_kinesis_stream" "data_stream" {
  name             = "week-1-lab-stream"
  shard_count      = 1 # Intentional bottleneck for stress testing
  retention_period = 24

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]

  encryption_type = "KMS"
  kms_key_id      = "alias/aws/kinesis" # Using default alias for simplicity, or use aws_kms_key.data_key.arn
}

