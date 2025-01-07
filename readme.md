
# TangoFlux Web Interface

A web interface for TangoFlux text-to-audio generation model. Generate high-quality audio from text descriptions in a user-friendly interface.

<p align="center">
  <img src="/templates/generating.png" alt="TangoFlux Web Interface Screenshot">
</p>

## Features

- 🎵 Generate audio from text descriptions
- ⚡ Fast generation (3-4 seconds per audio)
- 🎚️ Global audio player with volume control
- 🔄 Generate multiple sounds at once
- ⏱️ Adjustable duration (1-30 seconds)
- 💾 Download generated audio files
- 🎯 Clean and intuitive interface

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/tangoflux-web.git](https://github.com/tibzejoker/tangoflux-web)
cd tangoflux-web
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5566`

## Requirements

- Flask==3.0.0
- torch>=2.0.0
- torchaudio==2.1.1
- accelerate
- TangoFlux (installed from GitHub)

## Usage

1. Enter your text description
2. Set the desired duration (1-30 seconds)
3. Choose how many variations to generate (1-10)
4. Click "Generate Sound"
5. Use the global player to listen to your generations
6. Download the audio files you want to keep

## License

This project is licensed under the same terms as TangoFlux:
- Non-commercial use only (research/academic purposes)
- Subject to the Stability AI Community License Agreement
- See [TangoFlux License](https://github.com/declare-lab/TangoFlux#license) for full details

## Credits

This project uses:
- [TangoFlux](https://github.com/declare-lab/TangoFlux) - The core text-to-audio generation model

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- TangoFlux team for creating the amazing text-to-audio model
- Stability AI for supporting the research
```

This README includes:
1. Brief description
2. Screenshot placeholder
3. Features list
4. Installation instructions
5. Requirements
6. Usage guide
7. License information
8. Credits
9. Contributing guidelines
10. Acknowledgments
