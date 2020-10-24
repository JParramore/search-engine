import React from 'react';
import { Row, Col, Divider } from 'antd';
import SearchContainer from './Components/SearchContainer';

function App() {

  return (
    <>
      <Divider orientation="left">search-engine</Divider>
      <Row justify="center" align="middle">
        <Col span={16}>
          <SearchContainer />
        </Col>
      </Row>
    </>
  );
}

export default App;
