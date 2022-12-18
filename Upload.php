<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8" />

  <script type="text/javascript" src="http://static.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js"></script>
  <script type="text/javascript" src="http://static.robotwebtools.org/roslibjs/current/roslib.min.js"></script>

  <script type="text/javascript">
        function Publish_data() {
            // Connecting to ROS
            // -----------------
            var ros = new ROSLIB.Ros({
            url : 'ws://localhost:9090'
            });

            ros.on('connection', function() {
            console.log('Connected to websocket server.');
            });

            ros.on('error', function(error) {
            console.log('Error connecting to websocket server: ', error);
            });

            ros.on('close', function() {
            console.log('Connection to websocket server closed.');
            });

            // Publishing a Topic
            // ------------------

            var cmdVel = new ROSLIB.Topic({
            ros : ros,
            name : '/cmd_vel',
            messageType : 'geometry_msgs/Twist'
            });

            var twist = new ROSLIB.Message({
            shape: "circle",
            center: "255, 255",
            
            });
            cmdVel.publish(twist);
        }
    </script>

 </head>

  <body>
    <h1>Simple roslib Example</h1>
    <p>Check your Web Console for output.</p>
    <?php
        $flag = 0;
        if(!empty($_POST['image'])){
            if(file_put_contents(date("d-m-Y").'-'.time().'-'.rand(10000,100000).'.jpg',
            base64_decode($_POST['image']))){
                echo 'success';
                $flag = 1;
            }
            else echo 'Fail';
        }
        else echo 'No image';
        if ($flag) {
            echo $flag;
            $command = escapeshellcmd('read_img.py');
            $output = shell_exec($command);
            // Test output of python
            echo $output;
            echo '<script type="text/javascript">',
                'Publish_data()',
                '</script>';
        }
    ?>
    
  </body>
</html>