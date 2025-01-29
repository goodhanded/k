output arn {
  value = aws_dynamodb_table.dynamodb_table.arn
}
output name {
  value = aws_dynamodb_table.dynamodb_table.name
}
output stream_arn {
  value = aws_dynamodb_table.dynamodb_table.stream_arn
}