// 打字机
$.fn.autotype = function () {
	let $text = $(this);
	// console.log('this', this);
	let str = $text.html(); //返回被选 元素的内容
	let index = 0;
	let x = $text.html('');
	//$text.html()和$(this).html('')有区别
	let timer = setInterval(function () {
			//substr(index, 1) 方法在字符串中抽取从index下标开始的一个的字符
			let current = str.substr(index, 1);
			if (current == '<') {
				//indexOf() 方法返回">"在字符串中首次出现的位置。
				index = str.indexOf('>', index) + 1;
			} else {
				index++;
			}
			//console.log(["0到index下标下的字符",str.substring(0, index)],["符号",index & 1 ? '_': '']);
			//substring() 方法用于提取字符串中介于两个指定下标之间的字符
			$text.html(str.substring(0, index) + (index & 1 ? '__' : ''));
			if (index >= str.length) {
				clearInterval(timer);
			}
		},
		100);
};
$("#autotype").autotype();

// canvas
try {
	if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {

	} else {
		$(function () {
			let canvas = document.querySelector('canvas'),
				ctx = canvas.getContext('2d')
			canvas.width = $(window).width();
			canvas.height = $(window).height();
			ctx.lineWidth = .3;
			ctx.strokeStyle = (new Color(150)).style;

			let mousePosition = {
				x: 30 * canvas.width / 100,
				y: 30 * canvas.height / 100
			};

			let dots = {
				nb: 250,
				distance: 100,
				d_radius: 150,
				array: []
			};

			function colorValue(min) {
				return Math.floor(Math.random() * 255 + min);
			}

			function createColorStyle(r, g, b) {
				return 'rgba(' + r + ',' + g + ',' + b + ', 0.8)';
			}

			function mixComponents(comp1, weight1, comp2, weight2) {
				return (comp1 * weight1 + comp2 * weight2) / (weight1 + weight2);
			}

			function averageColorStyles(dot1, dot2) {
				let color1 = dot1.color,
					color2 = dot2.color;

				let r = mixComponents(color1.r, dot1.radius, color2.r, dot2.radius),
					g = mixComponents(color1.g, dot1.radius, color2.g, dot2.radius),
					b = mixComponents(color1.b, dot1.radius, color2.b, dot2.radius);
				return createColorStyle(Math.floor(r), Math.floor(g), Math.floor(b));
			}

			function Color(min) {
				min = min || 0;
				this.r = colorValue(min);
				this.g = colorValue(min);
				this.b = colorValue(min);
				this.style = createColorStyle(this.r, this.g, this.b);
			}

			function Dot() {
				this.x = Math.random() * canvas.width;
				this.y = Math.random() * canvas.height;

				this.vx = -.5 + Math.random();
				this.vy = -.5 + Math.random();

				this.radius = Math.random() * 2;

				this.color = new Color();
			}

			Dot.prototype = {
				draw: function () {
					ctx.beginPath();
					ctx.fillStyle = this.color.style;
					ctx.arc(this.x, this.y, this.radius, 0, Math.PI, false);
					ctx.fill();
				}
			};

			function createDots() {
				for (i = 0; i < dots.nb; i++) {
					dots.array.push(new Dot());
				}
			}

			function moveDots() {
				for (i = 0; i < dots.nb; i++) {

					let dot = dots.array[i];

					if (dot.y < 0 || dot.y > canvas.height) {
						dot.vx = dot.vx;
						dot.vy = -dot.vy;
					} else if (dot.x < 0 || dot.x > canvas.width) {
						dot.vx = -dot.vx;
						dot.vy = dot.vy;
					}
					dot.x += dot.vx;
					dot.y += dot.vy;
				}
			}

			function connectDots() {
				for (i = 0; i < dots.nb; i++) {
					for (j = 0; j < dots.nb; j++) {
						i_dot = dots.array[i];
						j_dot = dots.array[j];

						if ((i_dot.x - j_dot.x) < dots.distance && (i_dot.y - j_dot.y) < dots.distance && (i_dot.x - j_dot.x) > -dots.distance && (i_dot.y - j_dot.y) > -dots.distance) {
							if ((i_dot.x - mousePosition.x) < dots.d_radius && (i_dot.y - mousePosition.y) < dots.d_radius && (i_dot.x - mousePosition.x) > -dots.d_radius && (i_dot.y - mousePosition.y) > -dots.d_radius) {
								ctx.beginPath();
								ctx.strokeStyle = averageColorStyles(i_dot, j_dot);
								ctx.moveTo(i_dot.x, i_dot.y);
								ctx.lineTo(j_dot.x, j_dot.y);
								ctx.stroke();
								ctx.closePath();
							}
						}
					}
				}
			}

			function drawDots() {
				for (i = 0; i < dots.nb; i++) {
					let dot = dots.array[i];
					dot.draw();
				}
			}

			function animateDots() {
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				moveDots();
				connectDots();
				drawDots();

				requestAnimationFrame(animateDots);
			}

			$('canvas').on('mousemove', function (e) {
				mousePosition.x = e.pageX;
				mousePosition.y = e.pageY;
			});

			$('canvas').on('mouseleave', function (e) {
				mousePosition.x = canvas.width / 2;
				mousePosition.y = canvas.height / 2;
			});

			createDots();
			requestAnimationFrame(animateDots);
		});
	}
} catch (e) {
}
