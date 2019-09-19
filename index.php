<?php session_start();
?>

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>GesTickets2</title>
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/fonts/font-awesome.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Asul">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300">
    <link rel="stylesheet" href="assets/css/Auto-Modal-Popup.css">
    <link rel="stylesheet" href="assets/css/Button-Modal-popup-team-member-1.css">
    <link rel="stylesheet" href="assets/css/Button-Modal-popup-team-member.css">
    <link rel="stylesheet" href="assets/css/Dynamic-Table.css">
    <link rel="stylesheet" href="assets/css/Infobox-Responsiv.css">
    <link rel="stylesheet" href="assets/css/Navigation-Clean.css">
    <link rel="stylesheet" href="assets/css/Popup-Element-Overlay-1.css">
    <link rel="stylesheet" href="assets/css/Popup-Element-Overlay.css">
    <link rel="stylesheet" href="assets/css/styles.css">
	<link rel="shortcut icon" type="image/png" href="./img/favicon.png" id="favicon">
	<?php require("interract_bdd.php"); ?>
</head>

<body>
    <!-- Start: Navigation Clean -->
    <div>
        <nav class="navbar navbar-light navbar-expand-md navigation-clean">
            <div class="container"><a class="navbar-brand" href="#">Scientilivre</a></div>
        </nav>
    </div>
    <!-- End: Navigation Clean -->
    <!-- Start: 2 Row 4 Columns -->
    <div>
        <div class="container" style="width: 100%;padding: 0px;max-width: 100%;">
            <div class="row" style="/*wdth: 20%;*/">
                <div class="col-md-3" id="menu" style="background-color: #eee;text-align: right;padding-right: 0px;border-right-color: #bbb;">
                    <div style="padding-top: 5px;"><button class="btn btn-primary visible btn-menu" type="button">Ateliers</button>
                        <!-- Start: br Tag --><br>
                        <!-- End: br Tag --><button class="btn btn-primary btn-menu" type="button" >Horaires</button>
                        <!-- Start: br Tag --><br>
                        <!-- End: br Tag --><button class="btn btn-primary btn-menu" type="button" >Reservations</button></div>
                    <div class="row"></div>
                </div>
                <div class="col" id="pane1" style="background-color: #bbb;">
                    <!-- Start: Center Div -->
                    <div class="text-center">
                        <h1 id="pane1Title">Ateliers</h1>
						<div id="pane1Div"></div>
                    </div>
                    <!-- End: Center Div -->
                </div>
                <div class="col-md-3" id="pane2" style="background-color: #999;">
                    <!-- Start: Center Div -->
                    <div class="text-center">
                        <h1 id="pane2Title">Horaires</h1>
						<div id="pane2Div"></div>
                    </div>
                    <!-- End: Center Div -->
                </div>
                <div class="col-md-3" id="brief" style="background-color: #777;padding-bottom: 25px;">
                    <!-- Start: Center Div -->
                    <div class="text-center" style="padding-bottom: 10px;">
                        <h1>Panier</h1><button class="btn btn-primary" id="clearButton" type="button" style="padding-left: 45px;padding-right: 45px;font-size: 15px;border: none;background-color: #444;margin: 5px;">Effacer</button>
                        <!-- Start: br Tag --><br>
                        <!-- End: br Tag -->
                        <!-- Start: Button Modal popup team member -->
                        <div id="Modal-button-wrapper" class="text-center">
                            <!-- Start: Trigger Part Start --><a class="bs4_modal_trigger" href="#" data-modal-id="bs4_team" data-toggle="modal" style="padding-left: 48px;padding-right: 48px;padding-top: 2px;padding-bottom: 2px;border: none;background-color: #444;margin: 5px;font-size: 19px;color: white;text-transform: none;font-family: inherit;">Paiement</a>
                            <!-- End: Trigger Part Start -->
                            <!-- Start: Modal Part Start -->
                            <div id="bs4_team" class="modal fade bs4_modal bs4_blue bs4_bg_transp bs4_bd_black bs4_bd_semi_trnsp bs4_none_radius bs4_shadow_none bs4_center bs4_animate bs4FadeInDown bs4_duration_md bs4_easeOutQuint bs4_size_team" data-modal-backdrop="true"
                                data-show-on="click" data-modal-delay="false" data-modal-duration="false">
                                <!-- Start: Modal Dialog -->
                                <div class="modal-dialog">
                                    <!-- Start: Modal content -->
                                    <div class="modal-content">
                                        <!-- Start: Close Button --><a class="bs4_btn_x_out_shtr bs4_sq_txt_close bs4_team_btn" href="#" data-dismiss="modal"><strong>annuler</strong></a>
                                        <!-- End: Close Button -->
                                        <!-- Start: Body -->
                                        <div class="bs4_team_content bg-card1 bs4_team_txt">
                                            <h1>Paiement</h1>
											
												<div>
													Code Postal : <input id="postalCodeForm" name="codePostal" type="number" placeholder="31..." autofocus>
												</div>
												<div>
													<label for="modepaiment">Mode de paiement: </label>
													<label><input type="radio" name="modepaiement" value="espece" required checked/>Espèce</label>
													<label><input type="radio" name="modepaiement" value="cheque" required/>Chèque</label>
												</div>
												<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Nam nibh. Nunc varius facilisis eros. Sed erat. In in velit quis arcu ornare laoreet. Curabitur adipiscing luctus massa. Integer ut purus ac augue
												commodo commodo. Nunc nec mi eu justo tempor consectetuer.</p>
												<a class="bs4_btn_x_out_shtr" href="#" onclick="submitForm(<?php echo "'".session_id()."'";?>);">OK !</a></div>
											<form method="get" action="test.php" id="infoForm"></form>
                                        <!-- End: Body -->
                                    </div>
                                    <!-- End: Modal content -->
                                </div>
                                <!-- End: Modal Dialog -->
                            </div>
                            <!-- End: Modal Part Start -->
                        </div>
                        <!-- End: Button Modal popup team member -->
                    </div>
                    <!-- End: Center Div -->
                    <div class="row" style="background-color: #777;border-top-color: black;border-top: 1px;border-top-style: solid;">
                        <div class="col">
                            <div id="workshopList">
                                <p style="text-decoration:underline;">Ateliers</p>
								<p id="briefWorkshop" style="margin-left: 12px; font-size: 15px;" ></p>
                            </div>
                            <div id="reservation">
                                <p style="text-decoration:underline;">Reservations</p>
								<p id="briefReservation" ></p>
                            </div>
                            <div id="totalBlock">
                                <p>Total : <span id="total"></span> €</p>
								
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- End: 2 Row 4 Columns -->
    <script src="assets/js/jquery.min.js"></script>
    <script src="assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="assets/js/Auto-Modal-Popup.js"></script>
    <script src="assets/js/Button-Modal-popup-team-member.js"></script>
    <script src="assets/js/Dynamic-Table.js"></script>
    <script src="assets/js/Popup-Element-Overlay.js"></script>
    <span id="jqueryScript"><script src="assets/js/script.js"></script></span>
</body>

</html>