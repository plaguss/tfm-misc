---
marp: true
size: 16:9
paginate: true
theme: default
backgroundColor: #aed6f1 
color:  #1a5276 
math: katex

---

<!-- backgroundImage: "linear-gradient(135deg, #ffffff  0%, #aed6f1 100%)" -->

<!-- footer: 'Agustín Piqueres | Slides for CIDaEN's thesis | 2022' -->

<!-- 
_class: lead
_paginate: false
 -->

<style>
section { 
    font-size: 18px; 
}
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

<style scoped>section { font-size: 30px; }</style>

# Clasificación de movimientos de CrossFit: una aplicación con MoViNets <!-- fit -->


**Agustín Piqueres**

9/2022

![bg contain w:400 h:250](./assets/cidaen.png)
![bg contain w:400 h:250](./assets/logouclm.png)


---

<!-- footer: '![w:100 h:50](./assets/cidaen.png)' -->

<!-- 
_footer: '*https://arxiv.org/abs/1609.03499'
_paginate: true
 -->
# WaveNet*

Wavenet: A generative model for raw audio.
Aaron van den Oord, et al.
[@deepmind](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio),  2016

## Contributions
- Generative model for wave-form forms
- Capable of capturing important audio structure at many time-scales
- Conditioning support

Led to the **most natural-sounding** speech/audio synthesis at the time.

---

### 1.1 Motivación

<!-- 
header : 'Clasificación de movimientos de CrossFit: una aplicación con MoViNets.'
-->

---

### 1.2 Objetivos

---

### 1.3 Estructura del proyecto

---

### 2.1 Deep Learning


---

### 2.2 Cloud

---

### 2.3 Trabajos relacionados

---

### 3.1 Extracción y Recolección de datos

#### 2.1.1 Introducción


---

<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

### 3.1 Extracción y Recolección de datos
#### 3.1.2 Proceso de extracción

<p class="break"></p>

![center w:600 h:400](./assets/data_extraction_process_.png)

(Data extraction process)
</div>


---

### 3.1 Extracción y Recolección de datos

#### 3.1.3 Datos obtenidos

![image center](./assets/tabla_1_descriptive_stats.png)


---

### 3.2 Experimentación con Deep Learning

#### 3.2.1 Introducción


---

### 3.2 Experimentación con Deep Learning

#### 3.2.2 Preprocesado de los datos

![center w:1010 h:400](./assets/frames.png)

---

<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

### 3.2 Experimentación con Deep Learning

#### 3.2.3 Experimentos realizados y resultados


- 80% training (2164 clips), 20% test (541)

- Más apuntes

<p class="break"></p>

![center center w:600 h:300](./assets/sample_sizes.png)

* [*__Tensorboard.dev__*](https://tensorboard.dev/experiment/UXyupsnMQ2S74vdul3vdbw/#scalars)

</div>


---

<style scoped>section { justify-content: start; }</style>

<!-- https://github.com/marp-team/marp-core/issues/177 -->

### 3.2 Experimentación con Deep Learning

#### 3.2.4 Evaluación de los resultados


![bg contain w:300 h:200](./assets/heatmap_confusion.png)

![bg contain w:300 h:200](./assets/heatmap_correlations.png)


---

## 3. Desarrollo

### 3.3 Cloud y despliegue de la aplicación

#### 3.3.1 Introducción


---

<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>


<div class="twocols">

## 3.3  Desarrollo 
### 3.3 Cloud y despliegue de la aplicación
#### 3.3.2 Arquitectura cloud

<p class="break"></p>

![center w:600 h:400](./assets/cloud_diagram.png)(Diagrama Cloud) 
</div>


---

## 3. Desarrollo

### 3.3 Cloud y despliegue de la aplicación

#### 3.3.3 Resultado y funcionamiento

---

<style scoped>
/* Reset table styling provided by theme */
table, tr, td, th {
  all: unset;

  /* Override contextual styling */
  border: 0 !important;
  background: transparent !important;
}
table { display: table; }
tr { display: table-row; }
td, th { display: table-cell; }

/* ...and layout freely :) */
table {
  width: 100%;
}
td {
  text-align: center;
  vertical-align: middle;
}
</style>

<!-- REF: https://github.com/marp-team/marp-cli/issues/57 -->

<table>
  <tr>
    <td>thruster</td>
      <td><img src="./assets/thruster_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>chest-to-bar</td>
      <td><img src="./assets/chest-to-bar_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>double-unders</td>
      <td><img src="./assets/double-unders_1.gif" 
      width="180" 
      height="180"/>
      </td>
  </tr>
  <tr>
    <td>ghd</td>
      <td><img src="./assets/ghd_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>power clean</td>
      <td><img src="./assets/power-clean_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>deadlift</td>
      <td><img src="./assets/deadlift_1.gif" 
      width="180" 
      height="180"/>
      </td>
  </tr>
  <tr>
    <td>shspu</td>
      <td><img src="./assets/shspu_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>ohs</td>
      <td><img src="./assets/ohs_1.gif" 
      width="180" 
      height="180"/>
      </td>
    <td>bar-facing burpee</td>
      <td><img src="./assets/bar-facing-burpee_1.gif" 
      width="180" 
      height="180"/>
      </td>
  </tr>
</table>


---

## 4. Conclusiones


# Multi columns in Marp slide

<div class="columns">
<div>

## Column 1

Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas eveniet, corporis commodi vitae accusamus obcaecati dolor corrupti eaque id numquam officia velit sapiente incidunt dolores provident laboriosam praesentium nobis culpa.

</div>
<div>

## Column 2

Tempore ad exercitationem necessitatibus nulla, optio distinctio illo non similique? Laborum dolor odio, ipsam incidunt corrupti quia nemo quo exercitationem adipisci quidem nesciunt deserunt repellendus inventore deleniti reprehenderit at earum.

</div>
</div>

---

<style scoped>
div.twocols {
  margin-top: 35px;
  column-count: 2;
}
div.twocols p:first-child,
div.twocols h1:first-child,
div.twocols h2:first-child,
div.twocols ul:first-child,
div.twocols ul li:first-child,
div.twocols ul li p:first-child {
  margin-top: 0 !important;
}
div.twocols p.break {
  break-before: column;
  margin-top: 0;
}
</style>

# Tiling can improve the access pattern

<div class="twocols">

## LHS Title
- item

<p class="break"></p>

![right height:350px](./assets/bar-facing-burpee_1.gif)
</div>

---

Movimientoso
### bar-facing-burpee 

![center](./assets/bar-facing-burpee_1.gif)

--- 


