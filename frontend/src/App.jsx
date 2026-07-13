import { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");

  const [species, setSpecies] = useState("Neem");

  const [imageFile, setImageFile] = useState(null);

  const [imagePreview, setImagePreview] = useState(null);

  const [generatedImages, setGeneratedImages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [weather, setWeather] = useState([]);

  const [lighting, setLighting] = useState([]);

  const [cameraAngle, setCameraAngle] = useState([]);

  const [health, setHealth] = useState([]);

  const [season, setSeason] = useState([]);

  const [timeOfDay, setTimeOfDay] = useState([]);

  const [numImages, setNumImages] = useState(1);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setImageFile(file);

    setImagePreview(URL.createObjectURL(file));
  };

  const toggleSelection = (value, list, setter) => {
    if (list.includes(value)) {
      setter(list.filter((item) => item !== value));
    } else {
      setter([...list, value]);
    }
  };

  const generateImage = async () => {
    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("prompt", prompt);

      formData.append("generation_mode", imageFile ? "img2img" : "text2image");

      formData.append("species", species);

      formData.append("season", season.join(","));

      formData.append("weather", weather.join(","));

      formData.append("lighting", lighting.join(","));

      formData.append("camera_angle", cameraAngle.join(","));

      formData.append("health", health.join(","));

      formData.append("time_of_day", timeOfDay.join(","));

      formData.append("num_images", numImages);

      if (imageFile) {
        formData.append("image", imageFile);
      }

      const response = await axios.post(
        "http://127.0.0.1:8000/generate",
        formData
      );

      setGeneratedImages(response.data.images || []);

      alert("Generation completed!");

    } catch (err) {

      console.error(err);

      alert("Generation failed");

    } finally {

      setLoading(false);

    }
  };

  return (
    <div
      style={{
        maxWidth: "1000px",
        margin: "30px auto",
        padding: "25px",
        background: "white",
        borderRadius: "10px",
        boxShadow: "0 0 10px rgba(0,0,0,.1)"
      }}
    >

      <h1
        style={{
          textAlign: "center",
          marginBottom: "30px"
        }}
      >
        🌳 Synthetic Tree Generator
      </h1>

      <h3>Prompt</h3>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe your tree..."
        style={{
          width: "100%",
          height: "120px",
          padding: "10px",
          marginBottom: "20px"
        }}
      />

      <h3>Reference Image (Optional)</h3>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
      />

      {imagePreview && (

        <div style={{ marginTop: "20px" }}>

          <img
            src={imagePreview}
            alt="Preview"
            style={{
              width: "250px",
              borderRadius: "10px"
            }}
          />

        </div>

      )}

      <hr style={{ margin: "25px 0" }} />

      <h3>Species</h3>

      <select
        value={species}
        onChange={(e) => setSpecies(e.target.value)}
      >

        <option>Neem</option>

        <option>Mango</option>

        <option>Peepal</option>

        <option>Banyan</option>

      </select>
      <h3>Number of Images</h3>

      <select
        value={numImages}
        onChange={(e) => setNumImages(Number(e.target.value))}
      >
        {[1, 2, 3, 4].map((count) => (
          <option
            key={count}
            value={count}
          >
            {count}
          </option>
        ))}
      </select>
      <hr style={{ margin: "25px 0" }} />

      <h3>Season</h3>

      {["summer","winter","monsoon","autumn"].map((item)=>(
        <div key={item}>
          <label>
            <input
              type="checkbox"
              checked={season.includes(item)}
              onChange={()=>toggleSelection(item,season,setSeason)}
            />
            {" "}
            {item}
          </label>
        </div>
      ))}

      <hr style={{ margin: "25px 0" }} />

      <h3>Weather</h3>

      {["clear","rainy","foggy"].map((item)=>(
        <div key={item}>
          <label>
            <input
              type="checkbox"
              checked={weather.includes(item)}
              onChange={()=>toggleSelection(item,weather,setWeather)}
            />
            {" "}
            {item}
          </label>
        </div>
      ))}

      <hr style={{ margin: "25px 0" }} />

      <h3>Lighting</h3>

      {["morning","evening","night"].map((item)=>(
        <div key={item}>
          <label>
            <input
              type="checkbox"
              checked={lighting.includes(item)}
              onChange={()=>toggleSelection(item,lighting,setLighting)}
            />
            {" "}
            {item}
          </label>
        </div>
      ))}

      {/* ===== CONTINUE IN PART 2 ===== */}
            <hr style={{ margin: "25px 0" }} />

      <h3>Camera Angle</h3>

      {["front", "side", "top"].map((item) => (
        <div key={item}>
          <label>
            <input
              type="checkbox"
              checked={cameraAngle.includes(item)}
              onChange={() =>
                toggleSelection(item, cameraAngle, setCameraAngle)
              }
            />
            {" "}
            {item}
          </label>
        </div>
      ))}

      <hr style={{ margin: "25px 0" }} />

      <h3>Health</h3>

      {["healthy", "dry", "leaf_shedding"].map((item) => (
        <div key={item}>
          <label>
            <input
              type="checkbox"
              checked={health.includes(item)}
              onChange={() =>
                toggleSelection(item, health, setHealth)
              }
            />
            {" "}
            {item.replace("_", " ")}
          </label>
        </div>
      ))}

      <hr style={{ margin: "25px 0" }} />

      <h3>Time of Day</h3>

      {["morning", "afternoon", "evening"].map((item) => (
        <div key={item}>
          <label>
            <input
              type="checkbox"
              checked={timeOfDay.includes(item)}
              onChange={() =>
                toggleSelection(item, timeOfDay, setTimeOfDay)
              }
            />
            {" "}
            {item}
          </label>
        </div>
      ))}

      <hr style={{ margin: "30px 0" }} />

      <button
        onClick={generateImage}
        disabled={loading}
        style={{
          padding: "12px 30px",
          background: loading ? "#888" : "green",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: loading ? "not-allowed" : "pointer",
          fontSize: "16px",
        }}
      >
        {loading ? "Generating..." : "Generate"}
      </button>

      <hr style={{ margin: "30px 0" }} />

      <h2>Generated Images</h2>

      {generatedImages.length === 0 ? (
        <div
          style={{
            height: "250px",
            border: "2px dashed gray",
            borderRadius: "10px",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            color: "gray",
          }}
        >
          No image generated yet.
        </div>
      ) : (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "20px",
          }}
        >
          {generatedImages.map((image, index) => (
            <div key={index}>
              <img
                src={`http://127.0.0.1:8000${image}`}
                alt={`Generated ${index}`}
                style={{
                  width: "300px",
                  borderRadius: "10px",
                  border: "1px solid #ddd",
                }}
              />
            </div>
          ))}
        </div>
      )}

    </div>
  );
}

export default App;