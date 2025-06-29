import { render, screen, fireEvent } from "@testing-library/react";
import JsonToPdf from "../src/pages/JsonToPdf";
import { vi } from "vitest";

describe("JsonToPdf", () => {
  it("renders file input and button", () => {
    render(<JsonToPdf />);
    expect(screen.getByLabelText(/file/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Convert to PDF/i })
    ).toBeInTheDocument();
  });

  it("displays error for invalid file type", () => {
    render(<JsonToPdf />);
    const input = screen.getByLabelText(/file/i);
    const file = new File(["text"], "test.txt", { type: "text/plain" });
    fireEvent.change(input, { target: { files: [file] } });
    expect(
      screen.getByText("Please upload a valid JSON file")
    ).toBeInTheDocument();
  });

  it("enables convert button with valid JSON file", () => {
    render(<JsonToPdf />);
    const input = screen.getByLabelText(/file/i);
    const file = new File(['{"name": "John"}'], "test.json", {
      type: "application/json",
    });
    fireEvent.change(input, { target: { files: [file] } });
    expect(
      screen.queryByText("Please upload a valid JSON file")
    ).not.toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Convert to PDF/i })
    ).not.toBeDisabled();
  });
});
