resource "aws_lambda_function" "preprocess" {
  filename         = "lambda_function.zip"
  function_name    = "${var.project_name}-preprocess"
  role            = aws_iam_role.lambda_role.arn
  handler         = "index.handler"
  runtime         = "python3.9"
}

resource "aws_lambda_function" "polygon_converter" {
  filename         = "polygon_converter.zip"
  function_name    = "${var.project_name}-polygon-converter"
  role            = aws_iam_role.lambda_role.arn
  handler         = "index.handler"
  runtime         = "python3.9"
}
