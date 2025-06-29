import { render, screen } from "@testing-library/react";
import Home from "../src/pages/Home";

describe("Home", () => {
  it("renders welcome message", () => {
    render(<Home />);
    expect(
      screen.getByText("Welcome to the Converter App")
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Use the menu to explore available converters/)
    ).toBeInTheDocument();
  });
});
