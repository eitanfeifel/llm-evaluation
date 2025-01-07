"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const body_parser_1 = __importDefault(require("body-parser"));
const axios_1 = __importDefault(require("axios"));
const app = (0, express_1.default)();
const PORT = 3000;
// Middleware
app.use(body_parser_1.default.json());
app.use(express_1.default.static("public"));
// Endpoint to handle user input and call backend
app.post("/prompt", (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const userInput = req.body.prompt;
    try {
        const backendResponse = yield axios_1.default.post("http://localhost:8000/generate/", {
            prompt: userInput,
        });
        res.json(backendResponse.data);
    }
    catch (error) {
        res.status(500).json({ error: "Failed to get response from backend." });
    }
}));
// Start the server
app.listen(PORT, () => {
    console.log(`Frontend server running at http://localhost:${PORT}`);
});
// No module.exports needed; it's an ES module
