 resource "aws_volume_attachment" "ebs_att" {
   device_name = "/dev/sdf"
   volume_id   = aws_ebs_volume.example.id
   instance_id = aws_instance.app_server.id 
 }


 resource "aws_ebs_volume" "example" {
   availability_zone = "us-west-1b"
   size              = 1
}
