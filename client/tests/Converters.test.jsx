import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Converters from "../src/pages/Converters";

describe("Converters", () => {
  it("renders JSON to PDF link", () => {
    render(
      <MemoryRouter>
        <Converters />
      </MemoryRouter>
    );
    expect(screen.getByText("JSON to PDF")).toBeInTheDocument();
    expect(screen.getByText("JSON to PDF").closest("a")).toHaveAttribute(
      "href",
      "/converters/json-to-pdf"
    );
  });
});
