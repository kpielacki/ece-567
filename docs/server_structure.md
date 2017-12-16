# Server Structure

## Basic Structure
- Built through Flask web framework. Flask takes advantage of rendering and
  returning HTML templates through the Jinja2 library.
- MVC for SQL tables controlled by Flask-SQL-Alchemy and Flask Admin.
- User interactive dashboards handled through Plotly Dash.
- When mobile devices request for data it is done through making a mobile
  request route detailed in the Mobile Requests section.

## Folder Structure
- assets
  * admin
    - Flask Admin Requirements
  * css
    - Webpage CSS
  * fonts
    - Webpage Fonts
  * img
    - Webpage Images
  * js
    - Webpage Javascript Libraries
  * vendor
    - Bootstrap
- dashboards
  * Plotly Dash modules
- templates
  * HTML templates rendered through Jinja2
- views
  * Flask Admin Webpage Views

## Dashboards
- Uses Plotly Dash library to handle Javascript AJAX calls to backend.
- Dashboard defined through returning dash layout using HTML module to build.
  * When layout returned create route in main.py display_page function.
- Backend interaction done through @app.callback() decorator
- Create interactive JS elements through dcc.Input
- Return interactive JS elements through dcc.Output

## Plotly HTML
- Instead of writing HTML or using an HTML templating engine, you compose your
  layout using Python structures with the dash-html-components library
```
import dash_html_components as html

html.Div([
    html.H1('Hello Dash'),
    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P('This conversion happens behind the scenes by Dash's JavaScript
front-end')
    ])
])
```

- Also possible to style and set class values of the HTML elements

### Python Code
```
import dash_html_components as html

html.Div([
    html.Div('Example Div', style={'color': 'blue', 'fontSize': 14}),
    html.P('Example P', className='my-class', id='my-p-element')
], style={'marginBottom': 50, 'marginTop': 25})
```

### Rendered HTML
```
<div style="margin-bottom: 50px; margin-top: 25px;">

    <div style="color: blue; font-size: 14px">
        Example Div
    </div>

    <p class="my-class", id="my-p-element">
        Example P
    </p>

</div>
```


## Jinja2
- For non interactive
