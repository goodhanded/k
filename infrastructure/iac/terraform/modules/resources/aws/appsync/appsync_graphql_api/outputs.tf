output id {
  value = aws_appsync_graphql_api.appsync_graphql_api.id
}
output endpoint {
  value = aws_appsync_graphql_api.appsync_graphql_api.uris["GRAPHQL"]
}