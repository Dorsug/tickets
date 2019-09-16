<?php
require('./lib/fpdf181/fpdf.php');
define('EURO', chr(128));

$pdf = new FPDF("L","mm","A5");
$pdf->AddPage();
$pdf->SetFont('Arial','B',16);

$pdf->Cell(40,10,'FACTURE',1,1,"C");

$pdf->SetFont('Arial','',12);

$pdf->Cell(0,10,"Paiement par ".$_GET["paymentMode"]." de ".$_GET["totalPrice"]." ".EURO);
$pdf->Ln();
//Moyen de Paiement

//Prix

//Code Postal

//Affichage des ateliers
$pdf->Cell(0,10,"Ateliers");

$pdf->Output("F","./data/".$_GET["sessionID"].".pdf");
?>