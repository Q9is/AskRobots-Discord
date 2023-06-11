# AskRobots-Discord

AskRobots-Discord is a scalable, plugin-oriented bot for Discord, offering dynamic 
interactions including AI-powered text conversations with GPT-3.5-Turbo and GPT-4 
integration.

## License
This project is licensed under the GNU Affero General Public License.

## Getting Started

### Prerequisites
Make sure you have installed Docker on your machine. If not, you can download it 
from [here](https://www.docker.com/products/docker-desktop).

### Build

To build the Docker image for this project, navigate to the project's root 
directory and run:

```bash
docker build -t askrobots-discord .
```

### Run

To run the bot, you need to supply it with the necessary environment variables. 
This can be done using an environment file (`.env`). Once you've set up your 
`.env` file, run:

```bash
docker run --env-file .env askrobots-discord
```

## Contribution

Contributions to AskRobots-Discord are always welcome. Whether it's enhancing 
existing features, adding new functionality, or fixing bugs, your input is 
highly appreciated. Please ensure you follow our code of conduct and contribution 
guidelines.

## Support

If you encounter any issues or require further information, please open an issue 
on this repository.

## Credits

This project is maintained by Dan Quellhorst. You can reach out at dan@quellhorst.com 
for any inquiries.