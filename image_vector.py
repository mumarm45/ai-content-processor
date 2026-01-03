# class ImageProcessor:
#     def init(self, image_size=(224, 224),
#                  norm_mean=[0.485, 0.456, 0.406],
#                  norm_std=[0.229, 0.224, 0.225]):
#         self.device = torch.device(“cuda” if torch.cuda.is_available() else “cpu”)
#         self.model = resnet50(pretrained=True).to(self.device)
#         self.model.eval()  // Set model to evaluation mode
#         // Image preprocessing pipeline
#         self.preprocess = transforms.Compose([
#             transforms.Resize(image_size),
#             transforms.ToTensor(),
#             transforms.Normalize(mean=norm_mean, std=norm_std),
#         ])
#     def encode_image(self, image_input, is_url=True):
#         try:
#             if is_url:
#                 // Fetch image from URL
#                 response = requests.get(image_input)
#                 image = Image.open(BytesIO(response.content)).convert(“RGB”)
#             else:
#                 // Load from local file
#                 image = Image.open(image_input).convert(“RGB”)
#             // Convert image to Base64
#             buffered = BytesIO()
#             image.save(buffered, format=”JPEG”)
#             base64_string = base64.b64encode(buffered.getvalue()).decode(“utf-8”)
#             // Get feature vector using ResNet50
#             input_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
#             with torch.no_grad():
#                 features = self.model(input_tensor)
#             // Convert to NumPy array
#             feature_vector = features.cpu().numpy().flatten()
#             return {“base64”: base64_string, “vector”: feature_vector}
#         except Exception as e:
#             print(f”Error encoding image: {e}”)
#             return {“base64”: None, “vector”: None}

