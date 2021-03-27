<html lang="en"><head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="Martin Poláček">

    <title>Covid Log</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

</head>
<body style="">

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <div class="col-lg-6">
            <a class="navbar-brand" href="#">STI - Covid Log</a>
        </div>

        <div class="col-lg-6 text-right">

        </div>
    </div>
</nav>

<div class="container my-3">

    <div class="row">

        <table class="table table-striped">
            <tr>
                <th>Čas</th>
                <th>Typ logu</th>
                <th>Detaily</th>
            </tr>
            <?php
                include_once("db_conf.php"); // Include nastavení DB

                $query = "select * from log_data ORDER BY time desc";
                $result = mysqli_query($conn, $query) or die(mysqli_error($conn));
                while($row=mysqli_fetch_array($result,MYSQLI_BOTH)){
                    $toPrint = "<tr><td>" . $row["time"] . "</td><td>" . $row["type"] . "</td><td>" . $row["text"] . "</tr>";
                    echo $toPrint;
                }

            ?>
            </table>

    </div>

</div>


<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>



</body></html>