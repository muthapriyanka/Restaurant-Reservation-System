 resource "aws_launch_template" "example" {
   name_prefix   = "example"
   image_id      =  "ami-0d53d72369335a9d6" 
   instance_type = "t2.micro"
   user_data     = base64encode(<<-EOF
                  #!/bin/bash
                  sudo apt-get update
                  sudo apt-get install -y apache2
                  systmctl start apache2
                  systmctl enable apache2
                  echo "<h1> Welcome to my instance </h1>"> /var/www/html/index.html
                  mkdir -p /home/ubuntu/.ssh
                  echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDPRf6XX1ZpZ9bMPqx+NyXPkxP2c6EkG3/iIp9aAdhFh3XNQaDltJd8EwU7njteOlcpWS8ZV0CViC57NM7tPzrkpmOr6JvAUxV2Vv4V4/hCgLVOLkdidVITxofAQid1veSx21iG9jrHuh4S7QSohwirihjV9FB49c2XIsPJkrwAnFGUybsV7mtGXgEXLkFaOWp/ft8KXKElwL4Lb4F7Mxj0LiuKTVL11WAR19Ectker2WcZxmET1dTi0x80csFjG6QtQtY/Cxfkwl2oIvwyk+TcWogZOnPshTfoy4QhDSP5pPn3O6NE2wTTQwI5XpQWlaHVLBm2T5BRg8ZSW5kAvtlZApJzUj9VHrrAk3oZ72dYi7wyclc+7RAWt+wecvO+XQYTxXNexRZQX/jBLpKM3V7vDfgcJjGSl+Jx2q7z4WQ6oMctw3itr8tgciKjnWGXLKWL9bTiw7yysEaJPuQStpUTckT/E9odvcrj/RBq+yGf+cJWxnIUQbE7TJWyA/EtOdR/tL9Y7YAeaFYy7Bd5/VZMF0i1AImapf8dKi9f57MUkesKV8O1HOOJv1mzSTMnhXWEMtGs4ZGo2AB65eruYElR8cS+aTOL+mbh5t9UFho6Zzt/M6WtfB0CVULLs8HvDebU33p0agBtMPqg6n46gQtUhss/rk9IlsepqaTRnxJ9DQ==" >> /home/ubuntu/.ssh
                  chown -R ubuntu:ubuntu /home/ubuntu/.ssh
                  chmod 700 /home/ubuntu/.ssh
                  chmod 600 /home/ubuntu/.ssh/authorised_keys
                  EOF
                )
   vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]
 }

 resource "aws_autoscaling_group" "example" {
   vpc_zone_identifier = [aws_subnet.public.id]
   desired_capacity   = 2
   max_size           = 5
   min_size           = 1
 
   load_balancers = [aws_elb.example.name]
   launch_template {
     id      = aws_launch_template.example.id
     version = "$Latest"
   }
 }

 #Create a new load balancer
 resource "aws_elb" "example" {
   
   name               = "example-elb"
   subnets            = [aws_subnet.public.id]
   security_groups    = [aws_security_group.allow_ssh_http.id]

   health_check {
     healthy_threshold   = 3 # How many times the health check needs to succeed to be considered healthy
     unhealthy_threshold = 3 # How times the healthcheck needs to fail to mark the instance unhealthy and stop serving it traffic
     timeout             = 5 # how long to wait for the instance to respond to the health check in seconds
     target              = "HTTP:80/index.html" # What protocol, port, and path to test
     interval            = 30 # how often instances are probed in seconds
   }
  
   listener {
     instance_port     = 80 # What port the instances are listening on
     instance_protocol =  "HTTP"# What protocol the instances are using to serve traffic
     lb_port           = 80 # What port the load balancer is listening on
     lb_protocol       =  "HTTP"# What protocol the load balancer is using to serve traffic
   }
     #security_groups = [aws_security_group.allow_ssh.id]
 }

