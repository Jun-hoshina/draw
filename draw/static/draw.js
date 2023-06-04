var mamDraw = [];
mamDraw.isMouseDown = false;
mamDraw.position = [];
mamDraw.position.x = 0;
mamDraw.position.y = 0;
mamDraw.position.px = 0;
mamDraw.position.py = 0;

window.addEventListener("load", function () {
  //初期設定
  mamDraw.canvas = document.getElementById("drawcanvas");
  mamDraw.canvas.addEventListener("touchstart", onDown);
  mamDraw.canvas.addEventListener("touchmove", onMove);
  mamDraw.canvas.addEventListener("touchend", onUp);
  mamDraw.canvas.addEventListener("mousedown", onMouseDown);
  mamDraw.canvas.addEventListener("mousemove", onMouseMove);
  mamDraw.canvas.addEventListener("mouseup", onMouseUp);
  window.addEventListener("mousemove", StopShake);
  mamDraw.context = mamDraw.canvas.getContext("2d");
  mamDraw.context.strokeStyle = "#000000";
  mamDraw.context.lineWidth = 5;
  mamDraw.context.lineJoin = "round";
  mamDraw.context.lineCap = "round";
  document.getElementById("clearCanvas").addEventListener("click", clearCanvas);

});
function StopShake(event) {
  mamDraw.isMouseDown = false;
  //event.preventDefault();
  event.stopPropagation();
}
function onDown(event) {
  mamDraw.isMouseDown = true;
  mamDraw.position.px = event.touches[0].pageX - event.target.getBoundingClientRect().left - mamGetScrollPosition().x;
  mamDraw.position.py = event.touches[0].pageY - event.target.getBoundingClientRect().top - mamGetScrollPosition().y;
  mamDraw.position.x = mamDraw.position.px;
  mamDraw.position.y = mamDraw.position.py;
  drawLine();
  event.preventDefault();
  event.stopPropagation();
}
function onMove(event) {
  if (mamDraw.isMouseDown) {
    mamDraw.position.x = event.touches[0].pageX - event.target.getBoundingClientRect().left - mamGetScrollPosition().x;
    mamDraw.position.y = event.touches[0].pageY - event.target.getBoundingClientRect().top - mamGetScrollPosition().y;
    drawLine();
    mamDraw.position.px = mamDraw.position.x;
    mamDraw.position.py = mamDraw.position.y;
    event.stopPropagation();
  }
}
function onUp(event) {
  mamDraw.isMouseDown = false;
  event.stopPropagation();
}
function onMouseDown(event) {
  mamDraw.position.px = event.clientX - event.target.getBoundingClientRect().left;
  mamDraw.position.py = event.clientY - event.target.getBoundingClientRect().top;
  mamDraw.position.x = mamDraw.position.px;
  mamDraw.position.y = mamDraw.position.py;
  drawLine();
  mamDraw.isMouseDown = true;
  event.stopPropagation();
}
function onMouseMove(event) {
  if (mamDraw.isMouseDown) {
    mamDraw.position.x = event.clientX - event.target.getBoundingClientRect().left;
    mamDraw.position.y = event.clientY - event.target.getBoundingClientRect().top;
    drawLine();
    mamDraw.position.px = mamDraw.position.x;
    mamDraw.position.py = mamDraw.position.y;
    event.stopPropagation();
  }
}
function onMouseUp(event) {
  mamDraw.isMouseDown = false;
  event.stopPropagation();
}
function drawLine() {
  mamDraw.context.strokeStyle = "#000000";
  // mamDraw.context.strokeStyle = rgb(255,255,255);
  mamDraw.context.lineWidth = 10;
  mamDraw.context.lineJoin = "round";
  mamDraw.context.lineCap = "round";
  mamDraw.context.beginPath();
  mamDraw.context.moveTo(mamDraw.position.px, mamDraw.position.py);
  mamDraw.context.lineTo(mamDraw.position.x, mamDraw.position.y);
  mamDraw.context.stroke();
}
function clearCanvas() {
  // mamDraw.context.fillStyle = "rgb(255,255,255)";
  // mamDraw.context.fillRect(
  //   0, 0,
  //   mamDraw.canvas.getBoundingClientRect().width,
  //   mamDraw.canvas.getBoundingClientRect().height
  // )
  mamDraw.context.clearRect(
    0, 0, mamDraw.canvas.getBoundingClientRect().width, mamDraw.canvas.getBoundingClientRect().height
  );
  const button0 = document.getElementById("eraser");
  const button1 = document.getElementById("pensil");
  button0.disabled = false;
  button1.disabled = true;
  mamDraw.context.globalCompositeOperation = 'source-over';
}

// function mamGetScrollPosition() {
//   return {
//     "x": document.documentElement.scrollLeft || document.body.scrollLeft,
//     "y": document.documentElement.scrollTop || document.body.scrollTop
//   };
// }

// function StrIMG() {
//   var cvs = document.getElementById("drawcanvas");
//   var png = cvs.toDataURL();
//   console.log(png);
//   document.myform.submit();
//   document.getElementById("newImg").src = png;
//下の二つはhtmlにjsのデータを渡すためだけに書いてる
// }

function color(btnNum) {
  const button0 = document.getElementById("eraser");
  const button1 = document.getElementById("pensil");
  // クリックされたボタンが鉛筆だったら
  if (btnNum == 1) {
    button0.disabled = false;
    button1.disabled = true;
    mamDraw.context.globalCompositeOperation = 'source-over';
  }
  // クリックされたボタンが消しゴムだったら
  else if (btnNum == 0) {
    button0.disabled = true;
    button1.disabled = false;
    mamDraw.context.globalCompositeOperation = 'destination-out';
  }
}

function make(arr1, arr2) {
  const result = [];
  for (let i = 0; i < arr1.length; i++) {
    for (let j = 0; j < arr2.length; j++) {
      result.push([arr1[i], arr2[j]].join(""));
      // console.log([arr1[i], arr2[j]].join(""));
    }
  }
  // console.log(result);
  return result;
};

function send_img() {
  //canvas elementを取得
  var canvas = document.getElementById('drawcanvas');
  //base64データを取得（エンコード）
  var base64 = canvas.toDataURL('image/png');

  var fData = new FormData();
  fData.append('img', base64);

  // #ajax送信
  $.ajax({
    //画像処理サーバーに返す場合
    // url: 'http://127.0.0.1:5000/draw.png',
    url: "/draw/draw_png",
    type: 'POST',
    data: fData,
    contentType: false,
    processData: false,
    success: function (data, dataType) {
      //非同期で通信成功時に読み出される [200 OK 時]
      console.log('Success', data);
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
      //非同期で通信失敗時に読み出される
      console.log('Error : ' + errorThrown);
    }
  }).done(function (data) {
    var res = data.result;
    var index = data.index;
    console.log(res);
    console.log(index);

    console.log(index.length);
    var figure = [""]
    //indexに入っている[2,[1,7],8]]を218,278とする
    //すでに作ってある関数makeを使う
    //indexが-2だったら認識できませんと表示させる
    if (index.some(e => e == -2)) {
      figure = ["can't recognize"];
    } else {
      for (let i = 0; i < index.length; i++) {
        figure = make(figure, index[i]);
      }
    }
    // index=index.join('');
    result.innerHTML = figure;
    
    //候補が複数ある場合は候補として表示させる
    // $('#result').text(data.index).show();
    // 配列を数字にして最後にtext().showに入れる
  });
  event.preventDefault();
  //この関数必要なのかな?

  // location.href='/draw/draw_png'
  // 送信しても，この関数が終わるだけで，urlは同じままな気がするので追加

}

    // 消しゴムの機能をつけられるといいね

    //timerでたくさん回すとDSの百ます計算みたいに書いたらすぐ認識できる
