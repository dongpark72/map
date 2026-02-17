/*
 * 관련정보 ( 공시지가/실거래가 ,토지이력 · 특성, 건축물정보)
 */
$(document).ready(function(){
	//주소
	var newAddressNm=getNewAddressNm($("#pnu").val());
	$('.layer_content_wrap .addbox').text( newAddressNm);
	$('.layer_content_wrap .tbl04 .left').text( newAddressNm );
	
	//실거래 radio
	/*
	$("input[name=searchType]").change(function() {
		fn_getLandRealTranPriceList();
	});
	*/
	
	//click tab
	$('.relate_menu a').click(function(){
		var idx = $(".relate_menu a").index(this);
		fn_rowspanTable();
		fn_showRelate(idx);
	});
	
	//공시지가 loading
	$("#RelYearJigaList").html("<tr><td>"+loadingMsg+"</td></tr>");
	
	//실거래 loading
	if(fn_isPcSize())
		$("#real_table tbody").html("<tr><td colspan=8>"+loadingMsg+"</td></tr>");
	else
		$("#real_table tbody").html("<tr><td colspan=6>"+loadingMsg+"</td></tr>");
	
	//건축물 loading
	$("#tblBrFlrOulnInfo tbody").append("<tr><th colspan=7>"+loadingMsg+"</th></tr>");
	$("#tblBrFlrOulnInfoM tbody").append("<tr><th colspan=3>"+loadingMsg+"</th></tr>");
});

var httpRequestReal;
var httpRequestMove;
var httpRequestPos;
var httpRequestCha;
var httpRequestBuilding;

var tabId = 0;
var isLoadedTab0 = false;
var isLoadedTab1 = false;
var isLoadedTab2 = false;
var checking = true;

//pnu control added by tsjang (2023.06.21)
var nsdiPnu;
var realPriPnu;
var seyumPnu;
var upisPnu;

var getTomcatUrlConnector2 = "/dataapis/UrlConnector.jsp";
//var getTomcatUrlConnector2 = "https://www.eum.ne.kr:9005/MapPlan/UrlConnector.jsp";
//getTomcatUrlConnector2 = "/tomcat/UrlConnector.jsp"; //for dev

function fn_showRelate(val) {
	
	nsdiPnu = $("#pnu").val();
	realPriPnu = $("#pnu").val();
	seyumPnu = $("#pnu").val();
	upisPnu = $("#pnu").val();
	var chkSvc = "NSDI";
	var dataLoadYn = true; //서비스 중단인 경우 데이터를 로딩하지 않도록 설정
	
	if(val == '0') chkSvc = "REAL";
	else if(val == '1') chkSvc = "HIST";
	else if(val == '2') chkSvc = "NSDI";
	
	//연계 서비스 제어 추가 (by tsjang (2023.02.02)
	//if(!checking) return;
	$.ajax({
		type:"POST", 
    	url: context + "/ar/lu/luLandDetCheckAjaxXml.jsp",
    	dataType:"json",  
    	data:{
    		"link_sys_id" : chkSvc
    		, pnu : $("#pnu").val()
    	},
    	async: false,
    	error:function(){   
	        //console.log("예상치 못한 에러가 발생하였습니다.");   
	    }, 
        success : function(data){
        	var mapLuLandDetCheck = $.xml2json(data.mapLuLandDetCheck, true);
        	if(!mapLuLandDetCheck.node[0].text) {
	        	var closeSvc = mapLuLandDetCheck.node[0].linkSysId[0].text;
	        	var closeRsnDesc = mapLuLandDetCheck.node[0].closeRsnDesc[0].text;
	        	var closeRsnTy = mapLuLandDetCheck.node[0].closeRsnTy[0].text;
	        	//checking = false;
	        	
	        	//console.log(closeRsnTy+":"+closeRsnDesc);
	        	
	        	/*
	        	$(".city_box:eq(0) table tbody").empty();
	        	if(fn_isPcSize())
        			$(".city_box:eq(0) table tbody").append("<tr><td colspan='5'>"+closeRsnDesc+"</td></tr>");
        		else
        			$(".city_box:eq(0) table tbody").append("<tr><td>"+closeRsnDesc+"</td></tr>");
        		*/
	        	if(( closeSvc=='KREB')||( closeSvc=='REAL')) {
        			$("#rel_01").html("<div style='width:100%;text-align:center;padding: 70px 0;'>"+closeRsnDesc+"</div>");
        			dataLoadYn = false;
        		}
	        	if(( closeSvc=='HIST')) {
	        		$("#rel_02").html("<div style='width:100%;text-align:center;padding: 70px 0;'>"+closeRsnDesc+"</div>");
        			dataLoadYn = false;
	        	}
	        	if(( closeSvc=='NSDI')) {
	        		$("#rel_03").html("<div style='width:100%;text-align:center;padding: 70px 0;'>"+closeRsnDesc+"</div>");
        			dataLoadYn = false;
	        	}
        	}
        	
        	//added by tsjang(2023.06.21)
        	var mapPrevPnu = $.xml2json(data.mapPrevPnu, true);
        	if(!mapPrevPnu.node[0].text) {
        		var preLawdCd = mapPrevPnu.node[0].preLawdCd[0].text;
        		var nsdiYn = mapPrevPnu.node[0].nsdiYn[0].text;
        		var realPriYn = mapPrevPnu.node[0].realPriYn[0].text;
        		var seyumYn = mapPrevPnu.node[0].seyumYn[0].text;
        		var upisYn = mapPrevPnu.node[0].upisYn[0].text;
        		
        		//관련정보
        		if(nsdiYn == 'Y') {
        			nsdiPnu = preLawdCd;
        		}
        		//실거래가
        		if(realPriYn == 'Y') {
        			realPriPnu = preLawdCd;
        		}
        		//건축물대장
        		if(seyumYn == 'Y') {
        			seyumPnu = preLawdCd;
        		}
        		//UPIS
        		if(upisYn == 'Y') {
        			upisPnu = preLawdCd;
        		}
        	}
        },
        complete : function(){
        }
    });
	//if(!checking) return;
	//연계 서비스 제어 추가 end...

	//added by tsjang (2022.01.29)
	fn_loadRelateCode();
	
	tabId = val;
	
	//tab control
	$('.relate_menu li').removeClass('on');
	$('.relate_menu li a').removeClass('on');
	
	$('.relate_menu li:eq('+tabId+')').addClass('on');
	$('.relate_menu li a:eq('+tabId+')').addClass('on');
	
	tabPannel($('.relati_info'), 'tab_content', 0);
	tabPannelExt($('.relati_info'), 'tab_content', tabId);
	//loading proc
	if(dataLoadYn) setTimeout(fn_all_load, 100);

}

var codeXml;
function fn_loadRelateCode() {
	
	if(codeXml != undefined)
		return;
	
	$.ajax({
		type:"POST", 
    	url: context + "/ar/lu/luLandRelateCodeAjaxXml.jsp",
    	dataType:"json",
    	async: false,
    	error:function(){   
	        //console.log("예상치 못한 에러가 발생하였습니다.");   
	    }, 
        success : function(data){
        	var mapLuLandRelateCodeList = $.xml2json(data.mapLuLandRelateCodeList, true);
        	codeXml = mapLuLandRelateCodeList;
        	//console.log(codeXml);
        },
        complete : function(){
        }
    });
}

function fn_getRelateCodeName(year, cd_type, land_cd, land_nm){
	
	//console.log(year +":"+ cd_type +":"+  land_cd +":"+  land_nm);
	
	if(codeXml == undefined)
		return "-";
	
	//if(land_nm != undefined && land_nm != "" && land_nm != null)
		//return land_nm;
	
	var rtn = "-";
	for(i=0; i < codeXml.node.length; i++) {
		if( codeXml.node[i].appyYear[0].text <= year 
				&& codeXml.node[i].cdType[0].text == cd_type
				&& codeXml.node[i].landCd[0].text == land_cd
				) {
			rtn = codeXml.node[i].landNm[0].text;
		}
	}
	
	//없으면 처음값 유지
	if(land_nm != undefined && land_nm != "" && land_nm != null && rtn == "-") {
		rtn = land_nm;
	}
	
	return rtn;
}

function fn_all_load() {
	if(!isLoadedTab0 && tabId == 0) {
				
		//공시지가
		$.ajax({
	    	url: context + "/ar/lu/luLandDetYearAjax.jsp",
	    	data:{
	    		"pnu"		: $("#pnu").val(),
	    		"colSize"		: "4"
	    	},
	        type: "get",
	        contentType: "application/json; charset=euc-kr",
	        dataType: "html",
	        async: false,
	        success : function(data){
	        	$("#RelYearJigaList").html(data);
	        }
	    });
		
		//실거래
		$("#gimok").val( $("#present_class_val").val() );
		fn_getLandRealTranPriceList();
		
		isLoadedTab0 = true;
	}
	else if(!isLoadedTab1 && tabId == 1) {
		
		//소유권
		fn_getLandPossessionAttr();
		
		//토지이동
		fn_getLandMoveAttr();
		
		//토지특성
		fn_getLandCharacteristics();
		
		isLoadedTab1 = true;
	}	
	else if(!isLoadedTab2 && tabId == 2) {
		
		//건축물 정보
		fn_getLandBuildingInfo();
		
		isLoadedTab2 = true;
	}
}

//실거래 년단위
function fn_getLandRealTranPriceList() {
	//setTimeout(fn_getLandRealTranPriceListProc, 500);	
	fn_getLandRealTranPriceListProc();
}
function fn_getLandRealTranPriceListProc() {
	
	//clear tr
	$("#real_table tbody").empty();
	
	//최근 12개월
	/*
	if( $('input:radio[name="searchType"]:checked').val() == "now" ) {
		
		var nowDate = new Date();
		//for(var i=12; i>=1; i--) {
		//	nowDate.setMonth(nowDate.getMonth() - 1);
		//	var ymd = nowDate.getYear()+1900 + lpad(nowDate.getMonth()+1,2);
		//	getLandRealTranPriceInfo( ymd );
		//}		
		nowDate.setMonth(nowDate.getMonth());
		var ymd = nowDate.getYear()+1900 + lpad(nowDate.getMonth()+1,2);
		//console.log(ymd);
		getLandRealTranPriceInfo( ymd );
		
	}
	
	//연도별
	else {
		//for(var i=12; i>=1; i--) {
		//	getLandRealTranPriceInfo( $("#yyyy").val()+lpad(i,2) );
		//}
		//console.log($("#yyyy").val()+$("#mm").val());
		getLandRealTranPriceInfo( $("#yyyy").val()+$("#mm").val() );
	}
	*/
	getLandRealTranPriceInfo( $("#yyyy").val()+$("#mm").val() );
	
	//check empty
	/*
	if($("#real_table tbody tr").length == 0) {
		var newRowContent = "";
		newRowContent += "<tr>";
		if(fn_isPcSize())
			newRowContent += "<td colspan='8'>조회된 데이터가 없습니다</td>";
		else
			newRowContent += "<td colspan='6'>조회된 데이터가 없습니다</td>";
		newRowContent += "</tr>";
		$("#real_table tbody").append(newRowContent);
	}	
	*/
}

//실거래 월단위
var tmp;
function getLandRealTranPriceInfo(ymd) {
	//console.log(ymd);
	
	//loading
	$("#real_table tbody").html("<tr><td colspan=6>"+loadingMsg+"</td></tr>");
	
	var rtnCnt = 0;
	var PriceLawdNm = "";
	
	$.ajax({
		url : getTomcatUrlConnector + "?url="+getRTMSDataSvcLandTrade+"^serviceKey="+getNsdiKey+"|LAWD_CD="+realPriPnu.substring(0,5) + "|DEAL_YMD="+ymd,
		type: "get",
        contentType: "application/json; charset=euc-kr",
        dataType: "xml",
        //async: false,
		success : function(res) {
		
			tmp = $(res);
			rtnCnt = 0;
			PriceLawdNm = "";
			
			$("#real_table tbody").empty();
			
			//sorting
			items = fn_sortXml(res, "item", "dealMonth", "int", "dealDay", "int");
			
			$(items).each(function(idx){
				//console.log( $.trim($(this).find("법정동").text()).substring(0,$("#selUmd option:selected").text().length ) );
				PriceLawdNm = $.trim($(this).find("umdNm").text()).substring(0,$("#selUmd option:selected").text().length );
				
				if( $("#selUmd option:selected").text() == PriceLawdNm
					&& ( $("#gimok").val() == "" || $("#gimok").val() == $(this).find("jimok").text() )
					&& ( $("#ugroup").val() == "" || $(this).find("landUse").text().indexOf($("#ugroup").val()) > -1 )
					&& ( $("#uname").val() == "" || $(this).find("landUse").text() == $("#uname").val() )
				) {	
					
					var newRowContent = "";
					newRowContent += "<tr>";
					newRowContent += "<td>"+checkNull($(this).find("dealYear").text())+"."+checkNull($(this).find("dealMonth").text())+"."+checkNull($(this).find("dealDay").text())+"</td>";
					newRowContent += "<td>"+checkNull($(this).find("umdNm").text())+"</td>";
					newRowContent += "<td>"+checkNull($(this).find("jimok").text())+"</td>";
					newRowContent += "<td>"+checkNull($(this).find("landUse").text())+"</td>";
					newRowContent += "<td class='right'>"+checkNull($(this).find("dealArea").text())+"</td>";
					newRowContent += "<td class='right'>"+checkNull($(this).find("dealAmount").text())+"</td>";
					newRowContent += "</tr>";
					$("#real_table tbody").append(newRowContent);
					
					rtnCnt++;
				}
			});
				
			//console.log(rtnCnt);
			
			if(rtnCnt == 0) {
				//newRowContent = "<td colspan='8' style='border-left: none;'>조회된 데이터가 없습니다!</td>";				
				newRowContent = "<td colspan='6' style='border-left: none;'>"+$("#yyyy").val()+"년 "+$("#mm").val()+"월 실거래 내역이 없습니다. 조건을 변경하여 검색하여 주십시오.</td>";
				$("#real_table tbody").append(newRowContent);
			}
		}
	});
}

//실거래 용도지역 변경
function fn_changeUgroup() {
	
	var option = "";
	if( $("#ugroup").val() == "" ) {
		option += "<option value=''>전체</option>";
	}
	else if( $("#ugroup").val() == "주거지역" ) {
		option += "<option value=''>전체</option>";
		option += "<option value='제1종전용주거지역'>제1종전용주거지역</option>";
		option += "<option value='제2종전용주거지역'>제2종전용주거지역</option>";
		option += "<option value='제1종일반주거지역'>제1종일반주거지역</option>";
		option += "<option value='제2종일반주거지역'>제2종일반주거지역</option>";
		option += "<option value='제3종일반주거지역'>제3종일반주거지역</option>";
		option += "<option value='준주거지역'>준주거지역</option>";
	}
	else if( $("#ugroup").val() == "상업지역" ) {
		option += "<option value=''>전체</option>";
		option += "<option value='중심상업지역'>중심상업지역</option>";
		option += "<option value='일반상업지역'>일반상업지역</option>";
		option += "<option value='근린상업지역'>근린상업지역</option>";
		option += "<option value='유통상업지역'>유통상업지역</option>";
	} 
	else if( $("#ugroup").val() == "공업지역" ) {
		option += "<option value=''>전체</option>";
		option += "<option value='전용공업지역'>전용공업지역</option>";
		option += "<option value='일반공업지역'>일반공업지역</option>";
		option += "<option value='준공업지역'>준공업지역</option>";
	} 
	else if( $("#ugroup").val() == "녹지지역" ) {
		option += "<option value=''>전체</option>";
		option += "<option value='보전녹지지역'>보전녹지지역</option>";
		option += "<option value='생산녹지지역'>생산녹지지역</option>";
		option += "<option value='자연녹지지역'>자연녹지지역</option>";
	}
	else if( $("#ugroup").val() == "관리지역" ) {
		option += "<option value=''>전체</option>";
		option += "<option value='계획관리지역'>계획관리지역</option>";
		option += "<option value='생산관리지역'>생산관리지역</option>";
		option += "<option value='보전관리지역'>보전관리지역</option>";
	}
	else if( $("#ugroup").val() == "농림지역" ) {
		option += "<option value='농림지역'>농림지역</option>";
	} 
	else if( $("#ugroup").val() == "자연환경보전지역" ) {
		option += "<option value='자연환경보전지역'>자연환경보전지역</option>";
	}
	else if( $("#ugroup").val() == "개발제한구역" ) {
		option += "<option value='개발제한구역'>개발제한구역</option>";
	}
	else if( $("#ugroup").val() == "용도미지정" ) {
		option += "<option value='용도미지정'>용도미지정</option>";
	}
	else if( $("#ugroup").val() == "기타" ) {
		option += "<option value='기타'>기타</option>";
	}
	
	$("#uname").html(option);
	
	fn_getLandRealTranPriceList();
}

//토지이동
function fn_getLandMoveAttr() {
	
	/*by direct
	var url = getLandMoveAttr; //URL     
    var parameter = '?' + encodeURIComponent("authkey") +"="+encodeURIComponent(landMoveAttrKey); //authkey Key     
    parameter += "&" + encodeURIComponent("pnu") + "=" + encodeURIComponent(targetPnu); // 고유번호(8자리 이상)
    
    httpRequestMove = getXMLHttpRequest();
    httpRequestMove.onreadystatechange = getLandMoveAttrData; 
    httpRequestMove.open("GET", url + parameter, true);
	//httpRequestMove.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');     
    httpRequestMove.send('');
    */
	
	//by tomcat
	$.ajax({
		//url : getTomcatUrlConnector + "?url="+getLandMoveAttr+"^authkey="+encodeURIComponent(landMoveAttrKey)+"|pnu="+nsdiPnu+"|startDt=19000101|endDt="+getToday(),
		url : getTomcatUrlConnector2 + "?url="+getLandMoveAttr+"^key="+encodeURIComponent(landMoveAttrKey)+"|pnu="+nsdiPnu+"|startDt=19000101|endDt="+getToday()+"|domain=http://www.eum.go.kr|format=xml|numOfRows=30",
		type: "get",
        //contentType: "application/json; charset=euc-kr",
        dataType: "xml",
        //async: false,
		success : function(res) {
			
			var key1 = "ladMvmnDe";
			var key2 = "ladMvmnPrvonshCodeNm";
			var totalCount = $(res).find("totalCount").text();
			
			items = fn_sortXml(res, "field", key1, "int", key2, "str");
			$(items).each(function(idx){	
				//pc
  				var newRowContent = "";
  				newRowContent += "<tr>";      				
  				//if(i == (totalCnt-1)) newRowContent += "<td>현재</td>";
  				//else newRowContent += "<td></td>";
  				
  				if($(this).find("lndcgrCodeNm").text() != undefined) 
  					newRowContent += "<td>"+checkNull($(this).find("lndcgrCodeNm").text())+"</td>";
  				else
  					newRowContent += "<td></td>";
  				if($(this).find("lndpclAr").text() != undefined) 
  					newRowContent += "<td>"+comma($(this).find("lndpclAr").text())+"</td>";
  				else
  					newRowContent += "<td></td>";
  				if($(this).find("ladMvmnPrvonshCode").text() != undefined) 
  					newRowContent += "<td>"+checkNull(getLadMvmnPrvonshNm($(this).find("ladMvmnPrvonshCode").text(), $(this).find("ladMvmnPrvonshCodeNm").text()))+"</td>";
  				else
  					newRowContent += "<td></td>";
  				if($(this).find("ladMvmnDe").text() != undefined) 
  					newRowContent += "<td>"+checkNull($(this).find("ladMvmnDe").text())+"</td>";
  				else
  					newRowContent += "<td></td>";

  				newRowContent += "</tr>";
  				$("#land_table tbody").append(newRowContent);
  				
  				
  				
  				//mobile
  				var isFirst = true;
  				newRowContent = "";
  				
  				if(isFirst){ //first
  					newRowContent += "<tr><th scope=\"row\" colspan=\"2\" class=\"bg\">토지이동</th></tr>";
  					isFirst = false;
  				}
  				
  				newRowContent += "<tr>";
  				newRowContent += "<td class=\"bg\">지목</td>";
  				if($(this).find("lndcgrCodeNm").text() != undefined) 
  					newRowContent += "<td>"+checkNull($(this).find("lndcgrCodeNm").text())+"</td>";
  				else
  					newRowContent += "<td></td>";
  				newRowContent += "</tr>";
  				
  				newRowContent += "<tr>";
  				newRowContent += "<td class=\"bg\">면적</td>";
  				if($(this).find("lndpclAr").text() != undefined) 
  					newRowContent += "<td>"+comma($(this).find("lndpclAr").text())+"(㎡)</td>";
  				else
  					newRowContent += "<td></td>";
  				newRowContent += "</tr>";
  				
  				newRowContent += "<tr>";
  				newRowContent += "<td class=\"bg\">토지이동사유</td>";
  				if($(this).find("ladMvmnPrvonshCode").text() != undefined) 
  					newRowContent += "<td>"+checkNull(getLadMvmnPrvonshNm($(this).find("ladMvmnPrvonshCode").text(), $(this).find("ladMvmnPrvonshCodeNm").text()))+"</td>";
  				else
  					newRowContent += "<td></td>";
  				newRowContent += "</tr>";
  				
  				newRowContent += "<tr class=\"under_line\">";
  				newRowContent += "<td class=\"bg\">토지이동일</td>";
  				if($(this).find("ladMvmnDe").text() != undefined) 
  					newRowContent += "<td>"+checkNull($(this).find("ladMvmnDe").text())+"</td>";
  				else
  					newRowContent += "<td></td>";
  				newRowContent += "</tr>";

				$("#land_tableM tbody").append(newRowContent);
			});
  			
  			//토지이동 row 머지
  			$("#land_tr_move").attr("rowspan", (totalCount+1));
						
		}
	});

}
/*
function getLandMoveAttrData() {
	try {
		if (httpRequestMove.readyState == 4) {
  			if (httpRequestMove.status == 200) {
      			var xmlDoc = httpRequestMove.responseXML;
      			var totalCnt = xmlDoc.getElementsByTagName("field").length;
      			
      			for(var i=(totalCnt-1); i >= 0; i--) {
      				
      				//pc
      				var newRowContent = "";
      				newRowContent += "<tr>";      				
      				//if(i == (totalCnt-1)) newRowContent += "<td>현재</td>";
      				//else newRowContent += "<td></td>";
      				
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndcgrCodeNm")[0] != undefined) 
      					newRowContent += "<td>"+checkNull(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndcgrCodeNm")[0].textContent)+"</td>";
      				else
      					newRowContent += "<td></td>";
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndpclAr")[0] != undefined) 
      					newRowContent += "<td>"+comma(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndpclAr")[0].textContent)+"</td>";
      				else
      					newRowContent += "<td></td>";
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnPrvonshCodeNm")[0] != undefined) 
      					newRowContent += "<td>"+checkNull(getLadMvmnPrvonshNm(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnPrvonshCode")[0].textContent, xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnPrvonshCodeNm")[0].textContent))+"</td>";
      				else
      					newRowContent += "<td></td>";
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnDe")[0] != undefined) 
      					newRowContent += "<td>"+checkNull(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnDe")[0].textContent)+"</td>";
      				else
      					newRowContent += "<td></td>";

      				newRowContent += "</tr>";
      				$("#land_table tbody").append(newRowContent);
      				
      				
      				
      				//mobile
      				newRowContent = "";
      				
      				if(i == (totalCnt-1)) //first
      					newRowContent += "<tr><th scope=\"row\" colspan=\"2\" class=\"bg\">토지이동</th></tr>";
      				
      				newRowContent += "<tr>";
      				newRowContent += "<td class=\"bg\">지목</td>";
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndcgrCodeNm")[0] != undefined) 
      					newRowContent += "<td>"+checkNull(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndcgrCodeNm")[0].textContent)+"</td>";
      				else
      					newRowContent += "<td></td>";
      				newRowContent += "</tr>";
      				
      				newRowContent += "<tr>";
      				newRowContent += "<td class=\"bg\">면적</td>";
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndpclAr")[0] != undefined) 
      					newRowContent += "<td>"+comma(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("lndpclAr")[0].textContent)+"(㎡)</td>";
      				else
      					newRowContent += "<td></td>";
      				newRowContent += "</tr>";
      				
      				newRowContent += "<tr>";
      				newRowContent += "<td class=\"bg\">토지이동사유</td>";
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnPrvonshCodeNm")[0] != undefined) 
      					newRowContent += "<td>"+checkNull(getLadMvmnPrvonshNm(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnPrvonshCode")[0].textContent, xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnPrvonshCodeNm")[0].textContent))+"</td>";
      				else
      					newRowContent += "<td></td>";
      				newRowContent += "</tr>";
      				
      				newRowContent += "<tr class=\"under_line\">";
      				newRowContent += "<td class=\"bg\">토지이동일</td>";
      				if(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnDe")[0] != undefined) 
      					newRowContent += "<td>"+checkNull(xmlDoc.getElementsByTagName("field")[i].getElementsByTagName("ladMvmnDe")[0].textContent)+"</td>";
      				else
      					newRowContent += "<td></td>";
      				newRowContent += "</tr>";

					$("#land_tableM tbody").append(newRowContent);
      			}
      			
      			//토지이동 row 머지
      			$("#land_tr_move").attr("rowspan", (totalCnt+1));
				
  			} else {
	      		//alert("Fail: "+httpRequestMove.status);
	  		}
		}
	}catch(e) {
		//alert(e);			
	}
}
*/

//토지이동사유 대체
function getLadMvmnPrvonshNm_old(cd, nm) {
	var rtn = nm;
	
	if(cd == "10")
		rtn = "등록전환";
	else if(cd == "11")
		rtn = "등록전환되어 말소";
	else if(cd == "20")
		rtn = "필지 분할";
	else if(cd == "21")
		rtn = "필지 분할";
	else if(cd == "30")
		rtn = "필지 합병";
	else if(cd == "31")
		rtn = "필지 합병되어 말소";
	else if(cd == "43")
		rtn = "필지 지번변경";	
	else if(cd == "50")
		rtn = "행정구역명칭변경";
	else if(cd == "51")
		rtn = "행정관할구역변경";
	else if(cd == "52")
		rtn = "행정관할구역변경";
	else if(cd == "81" || cd == "82" || cd == "83" || cd == "84" || cd == "85" || cd == "90" || cd == "91")
		rtn = rtn.substring(0, rtn.indexOf("("));
	
	return rtn;
}
function getLadMvmnPrvonshNm(cd, nm) {
	/*
	var rtn = nm;
	
	if(cd == "1") rtn = "신규 등록";
	else if(cd == "2") rtn = "신규 등록(매립준공)";
	else if(cd == "10") rtn = "등록전환";
	else if(cd == "11") rtn = "등록전환되어 말소";
	else if(cd == "20") rtn = "필지 분할";
	else if(cd == "21") rtn = "필지 분할";
	else if(cd == "22") rtn = "분할개시 결정";
	else if(cd == "23") rtn = "분할개시 결정 취소";
	else if(cd == "30") rtn = "필지 합병";
	else if(cd == "31") rtn = "필지 합병되어 말소";
	else if(cd == "33") rtn = "지적재조사 예정지구 지정";
	else if(cd == "34") rtn = "지적재조사 예정지구 지정 폐지 ";
	else if(cd == "40") rtn = "지목변경";
	else if(cd == "41") rtn = "지목변경(매립준공)";
	else if(cd == "42") rtn = "해면성말소";
	else if(cd == "43") rtn = "지번변경";
	else if(cd == "44") rtn = "면적정정";
	else if(cd == "45") rtn = "경계정정";
	else if(cd == "46") rtn = "위치정정";
	else if(cd == "47") rtn = "지적복구";
	else if(cd == "48") rtn = "해면성복구";
	else if(cd == "49") rtn = "세계측지계좌표 변환";
	else if(cd == "50") rtn = "행정구역명칭변경";
	else if(cd == "51") rtn = "행정관할구역변경";
	else if(cd == "52") rtn = "행정관할구역변경";
	else if(cd == "53") rtn = "지적재조사 지구지정";
	else if(cd == "54") rtn = "지적재조사 지구지정폐지";
	else if(cd == "55") rtn = "지적재조사 완료";
	else if(cd == "56") rtn = "지적재조사로 폐쇄";
	else if(cd == "57") rtn = "지적재조사 경계미확정 토지";
	else if(cd == "58") rtn = "지적재조사 경계확정 토지";
	else if(cd == "60") rtn = "구획정리 시행신고";
	else if(cd == "61") rtn = "구획정리 시행신고폐지";
	else if(cd == "62") rtn = "구획정리완료";
	else if(cd == "63") rtn = "구획정리 되어 폐쇄";
	else if(cd == "65") rtn = "경지정리 시행신고";
	else if(cd == "66") rtn = "경지정리 시행신고폐지";
	else if(cd == "67") rtn = "경지정리 완료";
	else if(cd == "68") rtn = "경지정리 되어 폐쇄";
	else if(cd == "70") rtn = "축척변경 시행";
	else if(cd == "71") rtn = "축척변경 시행폐지";
	else if(cd == "72") rtn = "축척변경 완료";
	else if(cd == "73") rtn = "축척변경 되어 폐쇄";
	else if(cd == "74") rtn = "토지개발사업 시행신고";
	else if(cd == "75") rtn = "토지개발사업 시행신고폐지";
	else if(cd == "76") rtn = "토지개발사업 완료";
	else if(cd == "77") rtn = "토지개발사업으로 폐쇄";
	else if(cd == "80") rtn = "등록사항 정정대상 토지";
	else if(cd == "81") rtn = "등록사항 정정";
	else if(cd == "82") rtn = "도면등록사항정정";
	else if(cd == "83") rtn = "공유지연명부 등록사항정정";
	else if(cd == "84") rtn = "공유지(집합건물) 등록사항정정";
	else if(cd == "85") rtn = "경계점좌표등록부 등록사항정정";
	else if(cd == "90") rtn = "등록사항 말소";
	else if(cd == "91") rtn = "등록사항 회복";
	else rtn = rtn.substring(0, rtn.indexOf("("));
	*/
	
	rtn = fn_getRelateCodeName("0000", "LANDCD", cd, nm);
	return rtn;
}

//소유권
function fn_getLandPossessionAttr() {
	/*by direct
	var url = getLadfrlService+"?serviceKey="+getNsdiKey; //URL     
    var parameter = "&" + encodeURIComponent("pnu") + "=" + encodeURIComponent(targetPnu); // 고유번호(8자리 이상)
    
    httpRequestPos = getXMLHttpRequest();
    httpRequestPos.onreadystatechange = getLadfrlServiceUrlData; 
    httpRequestPos.open("GET", url + parameter, true);
	//httpRequestCha.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');     
    httpRequestPos.send('');
    */
    
    //by tomcat
	$.ajax({
		//url : getTomcatUrlConnector + "?url="+getLadfrlService+"^serviceKey="+encodeURIComponent(getNsdiKey)+"|pnu="+nsdiPnu,
		url : getTomcatUrlConnector2 + "?url="+getLadfrlService+"^key="+encodeURIComponent(landMoveAttrKey)+"|pnu="+nsdiPnu+"|domain=http://www.eum.go.kr|format=xml",
		type: "get",
        //contentType: "application/json; charset=euc-kr",
        dataType: "xml",
        //async: false,
		success : function(res) {
			
			//소유구분
  			$("#posesnSeCodeNm").text( checkNull($(res).find("posesnSeCodeNm").text()) );
  			$("#posesnSeCodeNmM").text( checkNull($(res).find("posesnSeCodeNm").text()) );
  			
  			//공유인수
  			$("#cnrsPsnCo").text( checkNull($(res).find("cnrsPsnCo").text()) );
  			$("#cnrsPsnCoM").text( checkNull($(res).find("cnrsPsnCo").text()) );
  			
  			//축척구분
  			/*
  			if($.trim($(res).find("ladFrtlScNm").text()) == "수치") {
  				$("#ladFrtlScNm").text( "1:500" );
      			$("#ladFrtlScNmM").text( "1:500" );
  			}
  			else {
      			$("#ladFrtlScNm").text( checkNull($(res).find("ladFrtlScNm").text()) );
      			$("#ladFrtlScNmM").text( checkNull($(res).find("ladFrtlScNm").text()) );
  			}
  			*/
  			$("#ladFrtlScNm").text( checkNull($(res).find("ladFrtlScNm").text()) );
  			$("#ladFrtlScNmM").text( checkNull($(res).find("ladFrtlScNm").text()) );
  				
  			//데이터기준일
  			$("#plastUpdtDt").text( checkNull($(res).find("lastUpdtDt").text()) );
  			$("#plastUpdtDtM").text( checkNull($(res).find("lastUpdtDt").text()) );
						
		}
	});
}
function getLadfrlServiceUrlData() {
	try {
		if (httpRequestPos.readyState == 4) {
  			if (httpRequestPos.status == 200) {
      			var res = httpRequestPos.responseXML;
      			
      			//소유구분
      			$("#posesnSeCodeNm").text( checkNull($(res).find("posesnSeCodeNm").text()) );
      			$("#posesnSeCodeNmM").text( checkNull($(res).find("posesnSeCodeNm").text()) );
      			
      			//공유인수
      			$("#cnrsPsnCo").text( checkNull($(res).find("cnrsPsnCo").text()) );
      			$("#cnrsPsnCoM").text( checkNull($(res).find("cnrsPsnCo").text()) );
      			
      			//축척구분
      			/*
      			if($.trim($(res).find("ladFrtlScNm").text()) == "수치") {
      				$("#ladFrtlScNm").text( "1:500" );
	      			$("#ladFrtlScNmM").text( "1:500" );
      			}
      			else {
	      			$("#ladFrtlScNm").text( checkNull($(res).find("ladFrtlScNm").text()) );
	      			$("#ladFrtlScNmM").text( checkNull($(res).find("ladFrtlScNm").text()) );
      			}
      			*/
      			$("#ladFrtlScNm").text( checkNull($(res).find("ladFrtlScNm").text()) );
      			$("#ladFrtlScNmM").text( checkNull($(res).find("ladFrtlScNm").text()) );
      				
      			//데이터기준일
      			$("#plastUpdtDt").text( checkNull($(res).find("lastUpdtDt").text()) );
      			$("#plastUpdtDtM").text( checkNull($(res).find("lastUpdtDt").text()) );

  			} else {
	      		//alert("Fail: "+httpRequestPos.status);
	  		}
		}
	}catch(e) {
		//alert(e);			
	}
}

//토지특성
function fn_getLandCharacteristics() {
	
	/* by direct
	var url = getLandCharacteristics; //URL     
    var parameter = '?' + encodeURIComponent("authkey") +"="+encodeURIComponent(landCharacteristicsKey); //authkey Key    
    parameter += "&" + encodeURIComponent("pnu") + "=" + encodeURIComponent(targetPnu); // 고유번호(8자리 이상)
    
    httpRequestCha = getXMLHttpRequest();
    httpRequestCha.onreadystatechange = getLandCharacteristicsData; 
    httpRequestCha.open("GET", url + parameter, true);
	//httpRequestCha.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');     
    httpRequestCha.send('');
    */
	
	//by tomcat
	//토지이력특성가져올때 numOfRows값을 기존 10 > 50으로 변경함. (사유 : totalCount가  11이고  결과값이 10개일때  가장최신 정보를 못가져옴.)
	$.ajax({
		//url : getTomcatUrlConnector + "?url="+getLandCharacteristics+"^authkey="+encodeURIComponent(landCharacteristicsKey)+"|pnu="+nsdiPnu+"|numOfRows=50",
		url : getTomcatUrlConnector2 + "?url="+getLandCharacteristics+"^key="+encodeURIComponent(landCharacteristicsKey)+"|pnu="+nsdiPnu+"|numOfRows=50|domain=http://www.eum.go.kr|format=xml",
		type: "get",
        //contentType: "application/json; charset=euc-kr",
        dataType: "xml",
        //async: false,
		success : function(res) {
			
			var totalCount = $(res).find("totalCount").text();
			
			$(res).find("field").each(function(idx){
				if(idx == eval(totalCount) - 1) {
					//지형높이
					codeNm = fn_getRelateCodeName( $(this).find("stdrYear").text(), "HGHT", $(this).find("tpgrphHgCode").text(), $(this).find("tpgrphHgCodeNm").text());
	      			$("#tpgrphHgCodeNm").text( checkNull(codeNm) );
	      			$("#tpgrphHgCodeNmM").text( checkNull(codeNm) );
	      			
	      			//지형형상
	      			codeNm = fn_getRelateCodeName( $(this).find("stdrYear").text(), "SHPE", $(this).find("tpgrphFrmCode").text(), $(this).find("tpgrphFrmCodeNm").text());
	      			$("#tpgrphFrmCodeNm").text( checkNull(codeNm) );
	      			$("#tpgrphFrmCodeNmM").text( checkNull(codeNm) );
	      			
	      			//도로접면
	      			codeNm = fn_getRelateCodeName( $(this).find("stdrYear").text(), "ROAD", $(this).find("roadSideCode").text(), $(this).find("roadSideCodeNm").text());
	      			$("#roadSideCodeNm").text( checkNull(codeNm) );
	      			$("#roadSideCodeNmM").text( checkNull(codeNm) );
	      			
	      			//데이터기준일
	      			$("#lastUpdtDt").text( checkNull($(this).find("lastUpdtDt").text()) );
	      			$("#lastUpdtDtM").text( checkNull($(this).find("lastUpdtDt").text()) );
				}
			});
						
		}
	});

}
/*
function getLandCharacteristicsData() {
	try {
		if (httpRequestCha.readyState == 4) {
  			if (httpRequestCha.status == 200) {
      			var xmlDoc = httpRequestCha.responseXML;
      			var totalCnt = xmlDoc.getElementsByTagName("field").length;
      			
      			//지형높이
      			$("#tpgrphHgCodeNm").text( xmlDoc.getElementsByTagName("tpgrphHgCodeNm")[totalCnt-1].textContent );
      			$("#tpgrphHgCodeNmM").text( xmlDoc.getElementsByTagName("tpgrphHgCodeNm")[totalCnt-1].textContent );
      			
      			//지형형상
      			$("#tpgrphFrmCodeNm").text( xmlDoc.getElementsByTagName("tpgrphFrmCodeNm")[totalCnt-1].textContent );
      			$("#tpgrphFrmCodeNmM").text( xmlDoc.getElementsByTagName("tpgrphFrmCodeNm")[totalCnt-1].textContent );
      			
      			//도로접면
      			$("#roadSideCodeNm").text( xmlDoc.getElementsByTagName("roadSideCodeNm")[totalCnt-1].textContent );
      			$("#roadSideCodeNmM").text( xmlDoc.getElementsByTagName("roadSideCodeNm")[totalCnt-1].textContent );
      			
      			//데이터기준일
      			$("#lastUpdtDt").text( xmlDoc.getElementsByTagName("lastUpdtDt")[totalCnt-1].textContent );
      			$("#lastUpdtDtM").text( xmlDoc.getElementsByTagName("lastUpdtDt")[totalCnt-1].textContent );

  			} else {
	      		//alert("Fail: "+httpRequestCha.status);
	  		}
		}
	}catch(e) {
		//alert(e);			
	}
}
*/

//건축물 정보
var BrTitleList = Array();
var BrTitleListCount = 0;
function fn_getLandBuildingInfo() {
	
	BrTitleList = Array();
	BrTitleListCount = 0;
	
	var pnu = seyumPnu;
	var parameter = "|sigunguCd="+pnu.substring(0,5);
	parameter += "|bjdongCd="+pnu.substring(5,10);    
	if(pnu.substring(10,11) == "1") parameter += "|platGbCd=0";
	else parameter += "|platGbCd=1";
	parameter += "|bun="+pnu.substring(11,15);
	parameter += "|ji="+pnu.substring(15);
	parameter += "|startDate=|endDate=|numOfRows=1000|pageNo=1";
	
	
	//총괄표제부
	$.ajax({
		url : getTomcatUrlConnector + "?url="+getBrRecapTitleInfo+"^serviceKey="+getNsdiKey+"|pnu="+parameter,
		type: "get",
        contentType: "application/json; charset=euc-kr",
        dataType: "xml",
		success : function(res) {
			
			$(res).find("item").each(function(idx){
				
				var newRowContent = "";
				newRowContent = "";
				newRowContent += "<tr class=\"center outline\" onClick=\"getLandBuildingDetail('"+BrTitleListCount+"');\" style=\"cursor:pointer\">";
				newRowContent += "<td>"+checkNull($(this).find("regstrKindCdNm").text())+"</td>";
				newRowContent += "<td>"+checkNull($(this).find("bldNm").text())+"</td>";
				newRowContent += "<td>"+checkNull($(this).find("dongNm").text())+"</td>";
				newRowContent += "<td class=\"mb\">"+checkNull($(this).find("etcPurps").text())+"</td>";
				newRowContent += "</tr>";
				$("#land_build tbody").append(newRowContent);
				
				BrTitleList[BrTitleListCount++] = $(this);
			});
			
		}
		, async: false
	});
	
	//표제부
	$.ajax({
		url : getTomcatUrlConnector + "?url="+getBrTitleInfo+"^serviceKey="+getNsdiKey+"|pnu="+parameter,
		type: "get",
        contentType: "application/json; charset=euc-kr",
        dataType: "xml",
		success : function(res) {
			
			var key1 = "mainAtchGbCd";
			var key2 = "dongNm";
			
			$(res).find("item").each(function(idx){
				//console.log( $(this).find(key1).text()+":"+$(this).find(key2).text() )
			});
			//console.log("------------------------");
			
			items = fn_sortXml(res, "item", key1, "int", key2, "str");
			
			$(items).each(function(idx){
				
				var newRowContent = "";
				newRowContent += "<tr class=\"center outline\" onClick=\"getLandBuildingDetail('"+BrTitleListCount+"');\" style=\"cursor:pointer\">";
				newRowContent += "<td>"+checkNull($(this).find("regstrKindCdNm").text())+"("+$(this).find("mainAtchGbCdNm").text()+")</td>";
				newRowContent += "<td>"+checkNull($(this).find("bldNm").text())+"</td>";
				newRowContent += "<td>"+checkNull($(this).find("dongNm").text())+"</td>";
				newRowContent += "<td class=\"mb\">"+checkNull($(this).find("etcPurps").text())+"</td>";
				newRowContent += "</tr>";
				$("#land_build tbody").append(newRowContent);
				
				BrTitleList[BrTitleListCount++] = $(this);
			});
			
			$(items).each(function(idx){
				//console.log( $(this).find(key1).text()+":"+$(this).find(key2).text() )
			});
			
		}
		, async: false
	});
	
	//정보가 있으면
	if(BrTitleListCount > 0) {
		
		//건축물정보
		getLandBuildingDetail(0);
		
		//층별현황
		//getLandFlrOulnInfo(0);
		
		fn_rowspanTable();
	}
	else {
		$("#rel_03").html("<div style='width:100%;text-align:center;padding: 70px 0;'>해당 필지에 건축물정보가 존재하지 않습니다.</div>");
	}
}

function fn_rowspanTable() {
	$('#tblBrFlrOulnInfo').rowspan(0);
	$('#tblBrFlrOulnInfoM').rowspan(0);
}

function fn_sortXml(res, item, key1, type1, key2, type2) {
	var items = $(res).find(item).get(); // Extract study elements into an array
	items.sort(function(a, b) { // And sort by their study_date elements
		if(type1 =="str") {
			var d1 = $(a).find(key1).text();
			var d2 = $(b).find(key1).text();
			return (d1 < d2 ? -1 : (d1 > d2 ? +1 : 0));
		}
		else if(type1 =="int") {
			var d1 = parseInt($(a).find(key1).text());
			var d2 = parseInt($(b).find(key1).text());
			return (d1 < d2 ? -1 : (d1 > d2 ? +1 : 0));
		}
	});

	items.sort(function(a, b) { // And sort by their study_date elements
		if(type2 =="str") {
			var d1 = $(a).find(key2).text();
			var d2 = $(b).find(key2).text();

			var d11 = $(a).find(key1).text();
			var d22 = $(b).find(key1).text();			

			if(d11 <= d22)
				return (d1 < d2 ? -1 : (d1 > d2 ? +1 : 0));
			else
				0;
		}
		else if(type2 =="int") {
			var d1 = parseInt($(a).find(key2).text());
			var d2 = parseInt($(b).find(key2).text());

			var d11 = parseInt($(a).find(key1).text());
			var d22 = parseInt($(b).find(key1).text());

			if(d11 <= d22)
				return (d1 < d2 ? -1 : (d1 > d2 ? +1 : 0));
			else
				return 0;
		}
	});
	
	return items;
}

function getLandBuildingDetail(idx) {
	//for pc
	$("#archArea").text( $(BrTitleList[idx]).find("archArea").text() );	
	if( $(BrTitleList[idx]).find("regstrKindCd").text() == "1" )		
		$("#totArea").text( comma($(BrTitleList[idx]).find("totArea").text()) );
	else
		$("#totArea").text( comma($(BrTitleList[idx]).find("totDongTotArea").text()) );	
	$("#vlRatEstmTotArea").text( comma($(BrTitleList[idx]).find("vlRatEstmTotArea").text()) );
	$("#bcRat").text( $(BrTitleList[idx]).find("bcRat").text() );
	$("#vlRat").text( $(BrTitleList[idx]).find("vlRat").text() );
	$("#useAprDay").text( toDate($(BrTitleList[idx]).find("useAprDay").text()) );
	
	//for mobile
	$("#archAreaM").text( comma($(BrTitleList[idx]).find("archArea").text()) );
	if( $(BrTitleList[idx]).find("regstrKindCd").text() == "1" )		
		$("#totAreaM").text( comma($(BrTitleList[idx]).find("totArea").text()) );
	else
		$("#totAreaM").text( comma($(BrTitleList[idx]).find("totDongTotArea").text()) );
	$("#vlRatEstmTotAreaM").text( $(BrTitleList[idx]).find("vlRatEstmTotArea").text() );
	
	//표제 선택
	$("#land_build tr td").removeClass("bg03 bold");
	$("#land_build tr:eq("+(2+parseInt(idx))+") td").addClass("bg03 bold");
	
	//건축물현황 or 층별현황
	getLandFlrOulnInfo(idx);
}

function getLandFlrOulnInfo(idx) {
	
	//건축물현황
	if( $(BrTitleList[idx]).find("regstrKindCd").text() == "1" ) {
	
		//clear : for pc
		$("#tblBrFlrOulnInfo tbody").empty();	
		
		//clear : for mobile
		var cnt = $("#tblBrFlrOulnInfoM tr").length - 5;
		for(i=0; i < cnt; i++) {
			$('#tblBrFlrOulnInfoM tr:last').remove();
		}
		
		var newRowContent = "";
		newRowContent += "<tr class=\"center\">";
		newRowContent += "	<th scope=\"row\" class=\"bg\"></th>";
		newRowContent += "	<td class=\"bg\">구분</td>";
		newRowContent += "	<td class=\"bg\">명칭</td>";
		newRowContent += "	<td class=\"bg\">구조</td>";
		newRowContent += "	<td class=\"bg\">층수</td>";
		newRowContent += "	<td class=\"bg\">용도</td>";
		newRowContent += "	<td class=\"bg\">면적(㎡)</td>";										
		newRowContent += "</tr>";				
		$("#tblBrFlrOulnInfo tbody").append(newRowContent);
		
		$(BrTitleList).each(function(i){			
			if($(this).find("regstrKindCd").text() == "3") { //표제부만 추가
				//pc
				newRowContent = "";
				newRowContent += "<tr class=\"center\">";
				newRowContent += "	<td scope=\"row\" class=\"bg\">건축물현황</td>";
				newRowContent += "	<td>"+checkNull($(this).find("mainAtchGbCdNm").text())+"</td>";
				newRowContent += "	<td>"+checkNull($(this).find("bldNm").text()+" "+$(this).find("dongNm").text())+"</td>";
				newRowContent += "	<td>"+checkNull($(this).find("strctCdNm").text())+"</td>";
				newRowContent += "	<td>지하 "+$(this).find("ugrndFlrCnt").text()+"층/지상 "+$(this).find("grndFlrCnt").text()+"층</td>";
				newRowContent += "	<td>"+checkNull($(this).find("etcPurps").text())+"</td>";
				newRowContent += "	<td>"+comma($(this).find("totDongTotArea").text())+"</td>";
				newRowContent += "</tr>";						
				$("#tblBrFlrOulnInfo tbody").append(newRowContent);				
				
				//mobile
				newRowContent = "";
				newRowContent += "<tr class=\"center\">";
				newRowContent += "	<td>"+checkNull($(this).find("bldNm").text()+" "+$(this).find("dongNm").text())+"</td>";
				newRowContent += "	<td>"+checkNull($(this).find("etcPurps").text())+"</td>";
				newRowContent += "	<td>"+comma($(this).find("totDongTotArea").text())+"</td>";
				newRowContent += "</tr>";						
				$("#tblBrFlrOulnInfoM tbody").append(newRowContent);
			}			
		});
		
		fn_rowspanTable();
	} 
	//층별현황	
	else { 
		
		var pnu = seyumPnu;
		var parameter = "|sigunguCd="+pnu.substring(0,5);
		parameter += "|bjdongCd="+pnu.substring(5,10);    
		if(pnu.substring(10,11) == "1") parameter += "|platGbCd=0";
		else parameter += "|platGbCd=1";
		parameter += "|bun="+pnu.substring(11,15);
		parameter += "|ji="+pnu.substring(15);
		parameter += "|startDate=|endDate=|numOfRows=1000|pageNo=1";
		
		//clear : for pc
		$("#tblBrFlrOulnInfo tbody").empty();
		
		//clear : for mobile
		var cnt = $("#tblBrFlrOulnInfoM tr").length - 5;
		for(i=0; i < cnt; i++) {
			$('#tblBrFlrOulnInfoM tr:last').remove();
		}
		
		//loading
		$("#tblBrFlrOulnInfo tbody").append("<tr><td colspan='7'>"+loadingMsg+"</td></tr>");
		$("#tblBrFlrOulnInfoM tbody").append("<tr><td colspan='3'>"+loadingMsg+"</td></tr>");
		
		$.ajax({
			url : getTomcatUrlConnector + "?url="+getBrFlrOulnInfo+"^serviceKey="+getNsdiKey+"|pnu="+parameter,
			type: "get",
	        contentType: "application/json; charset=euc-kr",
	        dataType: "xml",
			success : function(res) {
				
				//clear : for pc
				$("#tblBrFlrOulnInfo tbody").empty();
				
				var newRowContent = "";
				newRowContent += "<tr class=\"center\">";
				newRowContent += "	<th scope=\"row\" class=\"bg\"></th>";
				newRowContent += "	<td class=\"bg\">구분</td>";
				newRowContent += "	<td class=\"bg\">층별</td>";
				newRowContent += "	<td class=\"bg\">구조</td>";
				newRowContent += "	<td colspan=\"2\" class=\"bg\">용도</td>";
				newRowContent += "	<td class=\"bg\">면적(㎡)</td>";										
				newRowContent += "</tr>";				
				$("#tblBrFlrOulnInfo tbody").append(newRowContent);
				//$('#tblBrFlrOulnInfo').rowspan(0);
				
				
				//clear : for mobile
				var cnt = $("#tblBrFlrOulnInfoM tr").length - 5;
				for(i=0; i < cnt; i++) {
					$('#tblBrFlrOulnInfoM tr:last').remove();
				}				
				
				var key1 = "flrGbCd";
				var key2 = "flrNo";
				
				$(res).find("item").each(function(idx){
					//console.log( $(this).find(key1).text()+":"+$(this).find(key2).text() )
				});
				//console.log("------------------------");
				
				items = fn_sortXml(res, "item", key1, "int", key2, "int");
				
				//test = items;
				
				$(items).each(function(i){
										
					if( $(BrTitleList[idx]).find("dongNm").text() == $(this).find("dongNm").text() ) {
					
						//for pc
						newRowContent = "";
						newRowContent += "<tr class=\"center\">";
						newRowContent += "	<td scope=\"row\" class=\"bg\">층별현황</td>";
						newRowContent += "	<td>"+checkNull($(this).find("flrGbCdNm").text())+"</td>";
						newRowContent += "	<td>"+checkNull($(this).find("flrNoNm").text())+"</td>";
						newRowContent += "	<td>"+checkNull($(this).find("etcStrct").text())+"</td>";
						newRowContent += "	<td colspan=\"2\">"+checkNull($(this).find("etcPurps").text())+"</td>";
						newRowContent += "	<td>"+checkNull($(this).find("area").text())+"</td>";
						newRowContent += "</tr>";						
						$("#tblBrFlrOulnInfo tbody").append(newRowContent);
						
						//for mobile
						newRowContent = "";
						newRowContent += "<tr class=\"center\">";
						newRowContent += "	<td>"+checkNull($(this).find("flrNoNm").text())+"</td>";
						newRowContent += "	<td>"+checkNull($(this).find("etcPurps").text())+"</td>";
						newRowContent += "	<td>"+checkNull($(this).find("area").text())+"</td>";
						newRowContent += "</tr>";						
						$("#tblBrFlrOulnInfoM tbody").append(newRowContent);
					}
				});
				
				fn_rowspanTable();
						
				$(items).each(function(idx){
					//console.log( $(this).find(key1).text()+":"+$(this).find(key2).text() )
				});
						
			}
			//, async: false
		});
	}
	
	
	//층별현황 merge
	//$("#tblBrFlrOulnInfo").rowspan(0);
}


function fn_print() {
	  var divToPrint=document.getElementById('layer_body');
	  var newWin=window.open('','Print-Window');
	  newWin.document.open();
	  newWin.document.write('<html><link rel="stylesheet" href="'+context+'/css/reset.css"><link rel="stylesheet" href="'+context+'/css/common.css"><body onload="window.print()">'+divToPrint.innerHTML+'</body></html>');
	  newWin.document.close();
	  setTimeout(function(){newWin.close();},10);
}

function checkNull(str) {
	if($.trim(str) == "" || str.length == 0 || str == undefined) {
		return "-";
	}
	else {
		return str;
	}
}

function getToday(){
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1;    //1월이 0으로 되기때문에 +1을 함.
    var date = now.getDate();

    month = month >=10 ? month : "0" + month;
    date  = date  >= 10 ? date : "0" + date;
     // ""을 빼면 year + month (숫자+숫자) 됨.. ex) 2018 + 12 = 2030이 리턴됨.

    //console.log(""+year + month + date);
    return today = ""+year + month + date; 
}