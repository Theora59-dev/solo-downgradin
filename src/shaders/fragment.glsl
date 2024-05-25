#version 330

in vec2 fragmentTexCoord;
in vec2 texCoord;

out vec4 color;
uniform sampler2D imageTexture;

void main() {
    vec4 color = texture(imageTexture, texCoord);
    }
