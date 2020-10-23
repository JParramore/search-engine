import React from 'react';
import SearchContainer from '../SearchContainer'
import { shallow, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

global.fetch = jest.fn(() => Promise.resolve({
  json: () => Promise.resolve({
    response: [
      {
        'url': 'https://google.com/',
        'title': 'Google',
        'description': 'A description.',
        'highlight': 'Where the keywords were found.',
      },
      {
        'url': 'https://example.org/',
        'title': 'Example',
        'description': 'Another description.',
        'highlight': 'Where the keywords were found.',
      },
    ]
  }),
})
)

it('onChange of search makes api request with value', () => {
  let wrapper = shallow(<SearchContainer />);

  const event = {
    target: { value: 'test search' }
  };

  wrapper.find('Search').simulate('change', event);
  expect(fetch).toBeCalledWith(`/search?${new URLSearchParams({ q: event.target.value })}`);
})
