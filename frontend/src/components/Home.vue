// Home.vue

<template>
<div>
<div class="main">
  <div class="title">
    <h3>Image Classifier</h3>
  </div>

  <div class="panel">
    <input id="file-upload" class="hidden" type="file" accept="image/x-png,image/gif,image/jpeg" />
    <label for="file-upload" id="file-drag" class="upload-box">
      <div id="upload-caption">Drop image here or click to select</div>
      <img id="image-preview" class="hidden" />
    </label>
  </div>
  <div style="margin-bottom: 2rem;">
    <input type="button" value="Submit" class="button" onclick="submitImage();" />
    <input type="button" value="Clear" class="button" onclick="clearImage();" />
  </div>

  <div id="image-box" style="display:none;">
    <img id="image-display" />
    <div id="pred-result" class="hidden"></div>
    <svg id="loader" class="hidden" viewBox="0 0 32 32" width="32" height="32">
      <circle id="spinner" cx="16" cy="16" r="14" fill="none"></circle>
    </svg>
  </div>

  <div>
    <button v-on:click="draw" >drawChart</button>
    <div id="mychart" :style="{width: '300px', height: '300px'}"></div>
  </div>
  <div class="historyTable">
    
  </div>
</div>



</div>
</template>

<script>
  export default{
    data(){
      return{
        result: []
      }
    },
    mounted(){
      const s = document.createElement('script');
      s.type = 'text/javascript';
      s.src = '../../static/js/Home.js';
      document.body.appendChild(s);
      this.$emit('test')
      console.log("hello, world!")

    },
    methods:{
     draw:function(){
   			// this.count+=1
   			//监听自定义的事件
        // this.isShow = true
        show(mychart)
   			this.$on('increment', this.myEcharts)
   			this.$emit('increment')  //触发自定义的increment事件
   		},
      myEcharts(){
      // console.log(result)
      let xdata = []
      let ydata = []
      for(let val in result){
        // console.log(val)
        // console.log(Object.keys(result[val]))
        let keys = Object.keys(result[val])
        xdata.push(...keys)
        ydata.push(result[val][keys])

        // ydata[val] = result[val][1]
      }
      // console.log(xdata)
      // console.log(ydata)

		  // 基于准备好的dom，初始化echarts实例
		  var myChart = this.$echarts.init(document.getElementById('mychart'));

		  // 指定图表的配置项和数据
		  var option = {
			  title: {
				  text: '图像识别 top5'
			  },
			  tooltip: {},
			  legend: {
				  data:['概率']
			  },
			  xAxis: {
          data: xdata,
          axisLabel:{
            interval:0,
            rotate:45,
            margin:2,
            textStyle:{
              fontWeight:"bolder",
              color:"#000000"
            }
          }
			  },
			  yAxis: {},
			  series: [{
				  name: '概率',
				  type: 'bar',
				  data: ydata
			  }]
		  };

		  // 使用刚指定的配置项和数据显示图表。
		  myChart.setOption(option);
		  }
    }

  }
</script>

<style src="../../static/css/Home.css"></style>




