import { render, screen, fireEvent } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import JsonToPdf from '../src/pages/JsonToPdf.jsx';
import { MemoryRouter } from 'react-router-dom';

const server = setupServer(
  http.post('/api/convert/json-to-pdf', () => {
    return HttpResponse.text('PDF content', { status: 200 });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("JsonToPdf", () => {
  it("renders file input and button", () => {
    render(
      <MemoryRouter>
        <JsonToPdf />
      </MemoryRouter>
    );
    expect(screen.getByLabelText(/file/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Convert to PDF/i })
    ).toBeInTheDocument();
  });

  it("displays error for invalid file type", () => {
    render(
      <MemoryRouter>
        <JsonToPdf />
      </MemoryRouter>
    );
    const input = screen.getByLabelText(/file/i);
    const file = new File(["text"], "test.txt", { type: "text/plain" });
    fireEvent.change(input, { target: { files: [file] } });
    expect(
      screen.getByText(/Please upload a valid JSON file/i)
    ).toBeInTheDocument();
  });

  it("enables convert button with valid JSON file", () => {
    render(
      <MemoryRouter>
        <JsonToPdf />
      </MemoryRouter>
    );
    const input = screen.getByLabelText(/file/i);
    const file = new File(['{"name": "John"}'], "test.json", {
      type: "application/json",
    });
    fireEvent.change(input, { target: { files: [file] } });
    expect(
      screen.getByRole("button", { name: /Convert to PDF/i })
    ).not.toBeDisabled();
  });
});
