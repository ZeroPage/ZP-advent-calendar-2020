<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="index.css">
</head>
<body>
<h2><br><center>Zeropage 2020 Advent Calendar Write</center>
<form method="get" name="all" action="http://advent.kagamine.me:5001/create_post" target="iframe">

<?php
function select_month($mo=""){
    echo "<option value=' '>선택</option>";
    $tomonth = date("m");
    for($m=2;$m<=3;$m++){
        if($m == $mo){
            $date_month .= "<option value='$m' selected>$m</option>\n";
        }else{
            $date_month .= "<option value='$m'>$m</option>\n";
        }
    }
    return $date_month;
}
function select_day($da){
    echo "<option value=' '>선택</option>";
    $today = date("d");
    for($d=1;$d<=31;$d++){
        if ($d == $da){
            $date_day.="<option value='$d' selected>$d</option>\n";
        }else{
            $date_day.="<option value='$d'>$d</option>\n";
        }
    }
    return $date_day;
}
echo "<b>월 선택 </b>";
echo "<select name=\"month\">";
echo select_month("선택");
echo "</select>";
echo "<br>";

echo "<b>일 선택 </b>";
echo "<select name=\"day\">";
echo select_day("선택");
echo "</select>";
?>
<br>
<b>작성자 </b><input type="text" size=60 name="writer" class="input-field"><br /> 
<b>포스트 제목 </b><input type="text" size=60 name="title" class="input-field"><br /> 
<b>블로그 주소 </b><input type="text" size=60 name="addr" class="input-field"><br /> http:// 같은거 붙여주세요

<input type="submit" value="제출" >
<input type="reset" value="초기화">
<input type="button" value="이전 페이지로" onClick="history.go(-1)"> 
</form>
</html>
