L = 255;
[filename, pathname] = uigetfile({'*.bmp;*.jpg;*.png', 'Image Files(*.bmp, *.jpg, *.png)'}, 'Select an Image');
if isequal(filename, 0)
error('No image selected. Please select an image to continue.');
end
img = imread(fullfile(pathname, filename));
if size(img, 3) == 3
img = rgb2gray(img);
end
figure;
contrast_images = cell(1, 3);
for k = 1:3
r1 = input(['Enter the value for r1 for set ', num2str(k), ': ']);
s1 = input(['Enter the value for s1 for set ', num2str(k), ': ']);
r2 = input(['Enter the value for r2 for set ', num2str(k), ': ']);
s2 = input(['Enter the value for s2 for set ', num2str(k), ': ']);
a = s1 / r1;
b = (s2 - s1) / (r2 - r1);
c = (L - 1 - s2) / (L - 1 - r2);
output_image = zeros(size(img));
for i = 1:numel(img)
r = img(i);
if r <= r1
s = a * r;
elseif r > r1 && r <= r2
s = s1 + b * (r - r1);
else
s = s2 + c * (r - r2);
end
output_image(i) = round(s);
end
output_image = uint8(output_image);
contrast_images{k} = output_image;
subplot(1, 4, k + 1);
imshow(output_image);
title(sprintf('Set %d: r1=%.2f, s1=%.2f, r2=%.2f, s2=%.2f, a=%.3f,b=%.3f, c=%.3f', k, r1, s1, r2, s2, a, b, c));
end
binaryImg = contrast_images{3};
[height, width] = size(binaryImg);
encoded = [];
for i = 1:height
rowData = binaryImg(i, :);
pixelVal = rowData(1);
runLength = 0;
for j = 1:width
if rowData(j) == pixelVal
runLength = runLength + 1;
else
encoded = [encoded; pixelVal, runLength];
pixelVal = rowData(j);
runLength = 1;
end
end
encoded = [encoded; pixelVal, runLength];
end
fileID = fopen('encoded_runs.txt', 'w');
for i = 1:size(encoded, 1)
fprintf(fileID, '%d %d\n', encoded(i, 1), encoded(i, 2));
end
fclose(fileID);
fileID = fopen('compressed_image.bin', 'wb');
for i = 1:size(encoded, 1)
val = encoded(i, 1);
len = encoded(i, 2);
if len > 127
error('Run length exceeds 127.');
end
byte = bitshift(val, 7) + len;
fwrite(fileID, byte, 'uint8');
end
fclose(fileID);
originalSize = height * width;
compressedInfo = dir('compressed_image.bin');
if isempty(compressedInfo) || compressedInfo.bytes == 0
error('Compression failed.');
end
compressedSize = compressedInfo.bytes * 8;
compressionRatio = originalSize / compressedSize;
redundancy = 1 - (1 / compressionRatio);
fprintf('Compression Ratio: %.2f\n', compressionRatio);
fprintf('Redundancy: %.2f\n', redundancy);
fileID = fopen('compressed_image.bin', 'rb');
if fileID == -1
error('Compressed file not found.');
end
compressedData = fread(fileID, 'uint8');
fclose(fileID);
if isempty(compressedData)
error('No data in compressed file.');
end
decodedImg = [];
for i = 1:length(compressedData)
byte = compressedData(i);
pixelVal = bitshift(byte, -7);
runLength = bitand(byte, 127);
decodedImg = [decodedImg, repmat(pixelVal, 1, runLength)];
end
if numel(decodedImg) ~= originalSize
error('Decompressed data size mismatch.');
end
decodedImg = reshape(decodedImg, height, width);
subplot(1, 3, 1);
imshow(img); title('Original Image');
subplot(1, 3, 2);
imshow(decodedImg, []); title('Decompressed Image');
colormap gray;
subplot(1, 3, 3);
imshow(decodedImg, 'DisplayRange', []);
title('Compressed Image (Black/Greyed Out)');
disp('Decompression complete!');