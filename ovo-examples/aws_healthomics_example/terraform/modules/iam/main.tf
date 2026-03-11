resource "aws_iam_policy" "policy" {
  name        = var.policy_name
  description = var.policy_description
  policy      = var.policy
}

resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment" {
  role       = var.role_name
  policy_arn = aws_iam_policy.policy.arn
}