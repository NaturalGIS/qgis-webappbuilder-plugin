@VARIABLES@

var map = new ol.Map({
  layers: layersList,
  view: view
});


class TabbedApp extends React.Component {
  componentDidMount() {
    map.setTarget(document.getElementById('map'));
    map.getView().fit(originalExtent, map.getSize());
  }
  render() {
    return (
      <article>
        <nav role='navigation'>
          <div className='toolbar'>
            @LOGO@
            <a class="navbar-brand" href="#">@TITLE@</a>
            @TOOLBAR@
          </div>
        </nav>
        <div id='content'>
          <div className='row full-height'>
            <div className='col-md-8 full-height' id='tabs-panel'>
              <UI.SimpleTabs defaultActiveKey={1}>
                @PANELS@
              </UI.SimpleTabs>
            </div>
            <div className='col-md-16 full-height'>
              <div id='map'></div>
              @CONTROLS@
            </div>
          </div>
        </div>
      </article>
    );
  }
}

const nlMessages = {
  'geocoding.placeholder': 'Zoek op plaatsnaam'
};

React.render(<IntlProvider locale='nl' messages={nlMessages} >{() => (<TabbedApp />)}</IntlProvider>, document.body);



