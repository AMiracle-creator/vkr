document.addEventListener('DOMContentLoaded', function () {
    function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const forms = () => {
    initIndentificatorForm()
    initAgeForm()
    initDateForm()
}

const initIndentificatorForm = () => {
        const initYMap = async (fullPath) => {
            await ymaps.ready();

             const myMap = new ymaps.Map('map', {
            // Координаты центра карты.
            // Порядок по умолчанию: «широта, долгота».
            // Чтобы не определять координаты центра карты вручную,
            // воспользуйтесь инструментом Определение координат.
            center: [55.79, 49.10],
            // Уровень масштабирования. Допустимые значения:
            // от 0 (весь мир) до 19.
            zoom: 7
        });

        const fullPathByGuestList = [fullPath];

        console.log(fullPath)
        for (let i = 0; i < fullPathByGuestList.length; i++) {
             const myGeocoder = ymaps.geocode(fullPathByGuestList[i]);
                        myGeocoder.then(function (res) {
                            myMap.geoObjects.add(res.geoObjects);
                        })
            }
        }

        const renderTableItem = (item) => {
            return `<th scope="row">${item}</th>`
        }

        const renderTable = (data, id) => {
        const list = document.getElementById(id);
            const render_data = data[0].map(item => renderTableItem(item)).join("\n")

        list.innerHTML =  `<div class="loader">
                <div class="loader__legend">
                Данныe по гостинице ${data[0][0]}:
                </div>
            </div>

            <table class="table table_custom">
              <thead>
                <tr>
                  <th scope="col">id</th>
                  <th scope="col">Количество бронирований за все время</th>
                  <th scope="col">Адрес</th>
                  <th scope="col">Средний возраст клиентов</th>
                </tr>
              </thead>
              <tbody>
              <tr>
              ${render_data}
              </tr>
              </tbody>
            </table>

            <div class="single__about">
                <div style="width: 100%; align-items: center; justify-content: center; display: flex;padding: 20px 0">
                    <div id="map" style="width: 600px; height: 400px"></div>
                </div>
            </div>`

            initYMap(data[0][2])
    }

    const submitFormHandler = async () => {

            const hotel_id = document.getElementById('hotel_id')

        const response = await fetch('http://127.0.0.1:8000/indetifier_form/', {
            method: 'POST',
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({hotel_id: hotel_id.value})
        } )

        if (response.status === 200) {
            const resultData = await response.json()

            renderTable(resultData.hotel, 'result_identificator')
        }
    }


    const btnIdentificator = document.getElementById('identificator_btn')
    console.log(document.getElementById('identificator_btn'))
    btnIdentificator.addEventListener('click', submitFormHandler)
}

const initAgeForm = () => {
        const initYMap = async (fullPath) => {
             await ymaps.ready();

             const myMap = new ymaps.Map('map_range', {
            // Координаты центра карты.
            // Порядок по умолчанию: «широта, долгота».
            // Чтобы не определять координаты центра карты вручную,
            // воспользуйтесь инструментом Определение координат.
            center: [55.79, 49.10],
            // Уровень масштабирования. Допустимые значения:
            // от 0 (весь мир) до 19.
            zoom: 7
        });

        const fullPathByGuestList = fullPath;

        console.log(fullPath)
        for (let i = 0; i < fullPathByGuestList.length; i++) {
             const myGeocoder = ymaps.geocode(fullPathByGuestList[i]);
                        myGeocoder.then(function (res) {
                            myMap.geoObjects.add(res.geoObjects);
                        })
            }
        }

        const renderTableItemAge = (item) => {
            return item.map(small_item => `<th scope="row">${small_item}</th>`).join("\n")
        }

        const fullPaths = (res) => {
            const data_paths = []

            res.forEach(item => {
                data_paths.push(item[2])
            })

            return data_paths
        }

    const renderTableAges = (data, id) => {
            const list_age = document.getElementById(id)

        const render_data = data.map(item => `<tr>${renderTableItemAge(item)}</tr>`).join("\n")

        list_age.innerHTML = `
           <div class="loader">
                <div class="loader__legend">
                Данным критериям соответствуют гостиницы:
                </div>
            </div>

            <table class="table table_custom">
              <thead>
                <tr>
                  <th scope="col">id</th>
                  <th scope="col">Количество бронирований за все время</th>
                  <th scope="col">Адрес</th>
                  <th scope="col">Средний возраст клиентов</th>
                </tr>
              </thead>
              <tbody>
              ${render_data}
              </tbody>
            </table>

            <div class="single__about">
                <div style="width: 100%; align-items: center; justify-content: center; display: flex;padding: 20px 0">
                    <div id="map_range" style="width: 600px; height: 400px"></div>
                </div>
            </div>
        `
    }

    const submitFormHandlerAgeForm = async () => {

             const min_age = document.getElementById('min_age')
             const max_age = document.getElementById('max_age')

        const response = await fetch('http://127.0.0.1:8000/age_form/', {
            method: 'POST',
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({'min_age': min_age.value, 'max_age': max_age.value})
        } )

        if (response.status === 200) {
            const resultData = await response.json()
            console.log(resultData)

            renderTableAges(resultData.dataset, 'result_age')

            initYMap(fullPaths(resultData.dataset))
        }
    }


    const btnIdentificator = document.getElementById('age_btn')
    console.log(document.getElementById('age_btn'))
    btnIdentificator.addEventListener('click', submitFormHandlerAgeForm)
}

const initDateForm = () => {
        const renderTotal = (total) => {
            const total_block = document.getElementById('total_block')
            total_block.innerHTML = `<div class="loader">
                <div class="loader__legend">
                За данный период совершенно ${total} бронирований
                </div>
            </div>`
        }
        const submitFormHandlerDateForm = async () => {

             const from_date = document.getElementById('from_date')
             const to_date = document.getElementById('to_date')

        const response = await fetch('http://127.0.0.1:8000/date_form/', {
            method: 'POST',
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({'from_date': from_date.value, 'to_date': to_date.value})
        } )

        if (response.status === 200) {
            const resultData = await response.json()
            console.log(resultData)

            renderTotal(resultData.total, 'total_block')
        }
    }


    const btnDate = document.getElementById('date_btn')
    console.log(document.getElementById('date_btn'))
    btnDate.addEventListener('click', submitFormHandlerDateForm)
}

forms()
})