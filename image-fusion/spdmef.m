%% Function to achieve spdmef algorithm on the following paper:
%% "Robust Multi-Exposure Image Fusion: A Structural Patch Decomposition
%% Approach" - IEEE TRANSACTIONS ON IMAGE PROCESSING,VOL.26,NO.5,MAY 2017
%% Authors: Kede Ma, Hui Li, Hongwei Yong, Zhou Wang, Deui Meng, Lei Zhang
%%
%%
%% Created by Xiong Xiong, ChongQing University
%% 2017/10/4

function [] = spdmef()
global PATCH_SIDE_X;        % row
global PATCH_SIDE_Y;        % column
global PATCHES_WIDTH;       % column
global PATCHES_HEIGHT;      % row
global NR_CHANNEL;          % RGB
global NR_IMAGES;           % nummer of images
PATCH_SIDE_X = 4;  
PATCH_SIDE_Y = 4;  
PATCHES_WIDTH = 524;
PATCHES_HEIGHT = 388;
NR_CHANNEL = 3;     
NR_IMAGES = 3;

Image1 = imread('1.jpg');
Image2 = imread('2.jpg');
Image3 = imread('3.jpg');
Image = cell(3);
Image{1} = Image1;
Image{2} = Image2;
Image{3} = Image3;

patches = format_images(Image);
[g, p] = patches_mean_intensity(patches);
l_caret = calc_lcaret(g,p);
[c_caret, x_tilde] = calc_ccaret(patches, p);
s_caret = calc_scaret(patches, x_tilde);
Result = zeros(0);
for i = 1:PATCHES_HEIGHT
    tmp = zeros(0);
    for j = 1:PATCHES_WIDTH
        tmp_patch = uint8(c_caret(i,j) * s_caret{i,j} + l_caret(i,j));
        tmp = [tmp tmp_patch];
    end
    Result = [Result; tmp];
end
imwrite(Result, 'C:\Documents and Settings\Ene\×ÀÃæ\matlab-work\result.jpg');
end


%% calculate a matrix of s caret in patches size
%% input:   patches
%%          x_tilde
%% output:  s_caret
function [s_caret] = calc_scaret(patches, x_tilde)
global PATCHES_WIDTH;
global PATCHES_HEIGHT; 
s_caret = cell(PATCHES_HEIGHT, PATCHES_WIDTH);
for i = 1:PATCHES_HEIGHT
    for j = 1:PATCHES_WIDTH
        s_caret{i,j} = private_calc_scaret(patches{i,j}, x_tilde{i,j});
    end
end
end


%% calculate a matrix of c caret in patches size
%% input:   patches
%%          p_mean_inten
%% output:  c_caret
%%          x_tilde
function [c_caret, x_tilde] = calc_ccaret(patches, p_mean_inten)
global PATCHES_WIDTH;
global PATCHES_HEIGHT; 
c_caret = zeros(PATCHES_HEIGHT, PATCHES_WIDTH, 'double');
x_tilde = cell(PATCHES_HEIGHT, PATCHES_WIDTH);
for i = 1:PATCHES_HEIGHT
    for j = 1:PATCHES_WIDTH
        [c_caret(i,j), x_tilde{i,j}] = private_calc_ccaret(patches{i,j},p_mean_inten{i,j});
    end
end
end


%% calculate a matrix of l caret in patches size
%% input:   g_mean_inten - global mean intensity (one dimension)
%%          p_mean_inten - patches mean intensity (two dimension)
%% output:  l_caret - l caret matrix in patches size
function [l_caret] = calc_lcaret(g_mean_inten, p_mean_inten)
global PATCHES_WIDTH;
global PATCHES_HEIGHT; 
l_caret = zeros(PATCHES_HEIGHT, PATCHES_WIDTH, 'double');
for i = 1:PATCHES_HEIGHT
    for j = 1:PATCHES_WIDTH
        l_caret(i,j) = private_calc_lcaret(g_mean_inten,p_mean_inten{i,j});
    end
end
end


%% format all images
%% input:   image_matrix - matrix contains all images
%% output:  patches - matrix contains all images' patches
function [patches] = format_images(image_matrix)
global NR_IMAGES;
global PATCHES_WIDTH;
global PATCHES_HEIGHT; 
patches = cell(PATCHES_HEIGHT, PATCHES_WIDTH);
for i = 1:NR_IMAGES
    image_matrix{i} = private_split_image(image_matrix{i});
end
for i = 1:PATCHES_HEIGHT
    for j = 1:PATCHES_WIDTH
        tmp_patch = cell(NR_IMAGES);
        for k = 1:NR_IMAGES
            tmp_patch{k} = image_matrix{k}{i,j};
        end
        patches{i,j} = tmp_patch;
    end
end
end


%% calculate mean intensity of patches
%% input:   patches - matrix of patches after an image splitted
%% output:  g_mean_inten - global mean intensity
%%          p_mean_inten - matrix of patch mean intensity of patches
function [g_mean_inten, p_mean_inten] = patches_mean_intensity(patches)
global PATCHES_WIDTH;
global PATCHES_HEIGHT;
global NR_IMAGES;
p_mean_inten = cell(PATCHES_HEIGHT, PATCHES_WIDTH);
g_mean_inten = zeros(NR_IMAGES, 1, 'double');
for i = 1:PATCHES_HEIGHT
    for j = 1:PATCHES_WIDTH
        p_mean_inten{i,j} = private_patch_mean_intensity(patches{i,j});
        for k = 1:NR_IMAGES
            g_mean_inten(k) = g_mean_inten(k) + p_mean_inten{i,j}(k);
        end
    end
end
for i = 1:NR_IMAGES
    g_mean_inten(i) = g_mean_inten(i) / (PATCHES_WIDTH*PATCHES_HEIGHT);
end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% calculate each patch's c caret
%% input:   patch
%%          p_mean_inten
%% output:  c_caret
%%          x_tilde
function [c_caret, x_tilde] = private_calc_ccaret(patch, p_mean_inten)
global NR_IMAGES;
global PATCH_SIDE_X;
global PATCH_SIDE_Y;
global NR_CHANNEL;
c_caret = double(0);
x_tilde = zeros(NR_IMAGES, 1, 'double');
for h = 1:NR_IMAGES
    for i = 1:PATCH_SIDE_X
        for j = 1:PATCH_SIDE_Y
            for k = 1:NR_CHANNEL
                x_tilde(h)=x_tilde(h)+((patch{h}(i,j,k) - p_mean_inten(h))^2);
            end
        end
    end
end
for i = 1:NR_IMAGES
    x_tilde(i) = sqrt(x_tilde(i));
end
c_caret = max(x_tilde);
end


%% calculate each patch's s caret
%% input:   patch
%%          x_tilde
%% output:  s_caret
function [s_caret] = private_calc_scaret(patch, x_tilde)
global NR_IMAGES;
global PATCH_SIDE_X;
global PATCH_SIDE_Y;
global NR_CHANNEL;
s_caret = zeros(PATCH_SIDE_X, PATCH_SIDE_Y, NR_CHANNEL, 'double');
denomina = double(0);
for h = 1:NR_IMAGES
    %% need parameter of P in expression (5)
    s_caret = s_caret + (x_tilde(h) * patch{h});
    denomina = denomina + x_tilde(h);
end
s_caret = s_caret / denomina;
denomina = double(0);
for i = 1:PATCH_SIDE_X
    for j = 1:PATCH_SIDE_Y
        for k = 1:NR_CHANNEL
            denomina = denomina + (s_caret(i,j,k)^2);
        end
    end
end
denomina = sqrt(double(denomina));
s_caret = s_caret / denomina;
end


%% calculate l caret of a patch
%% input:   g_mean_inten - global mean intensity (one dimension)
%%          p_mean_inten - a patch mean intensity (one dimension)
%% output:  l_caret - l caret value
function [l_caret] = private_calc_lcaret(g_mean_inten, p_mean_inten)
global NR_IMAGES;
l_caret = double(0);
L = double(0);
molecule = double(0);
denomina = double(0);
sita_g = private_standard_deviation(g_mean_inten);
sita_p = private_standard_deviation(p_mean_inten);
if sita_g == 0
    sita_g = 1;
end
if sita_p == 0
    sita_p = 1;
end 
for i = 1:NR_IMAGES
    tmp1 = ((g_mean_inten(i)-128)^2) / (2*(sita_g^2));
    tmp2 = ((p_mean_inten(i)-128)^2) / (2*(sita_p^2));
    L = exp(double(0-double(tmp1)-double(tmp2)));
    molecule = molecule + (L * p_mean_inten(i));
    denomina = denomina + L;
end
if denomina == 0
    denomina = 1;
end
l_caret = double(molecule) / double(denomina);
end


%% calculate standard deviation
%% input:   matrix - a matrix
%% output:  result - result of standard deviation
function [result] = private_standard_deviation(matrix)
global NR_IMAGES;
mean = double(0);
result = double(0);
for i = 1:NR_IMAGES
    mean = mean + matrix(i);
end
mean = mean / NR_IMAGES;
for i = 1:NR_IMAGES
    result = result + ((matrix(i) - mean) ^ 2);
end
result = (double(double(result) / double(NR_IMAGES)))^0.5;
end


%% calculate mean intensity of a patch
%% input:   patch - a patch of patches
%% output:  mean_inten - matrix of mean intensity of current patch
function [mean_inten] = private_patch_mean_intensity(patch)
global PATCH_SIDE_X;
global PATCH_SIDE_Y;
global NR_CHANNEL;
global NR_IMAGES;
mean_inten = zeros(NR_IMAGES, 1, 'double');
for h = 1:NR_IMAGES
    for i = 1:PATCH_SIDE_X
        for j = 1:PATCH_SIDE_Y
            for k = 1:NR_CHANNEL
                mean_inten(h) = mean_inten(h) + patch{h}(i,j,k);
            end
        end
    end
    mean_inten(h) = mean_inten(h) / (PATCH_SIDE_X*PATCH_SIDE_Y*NR_CHANNEL);
end
end


%% split image to patches
%% input:   I - image matrix
%% output:  sub_patches - matrix of patches after an image splitted
function [sub_patches] = private_split_image(I)
global PATCH_SIDE_X;
global PATCH_SIDE_Y;
global PATCHES_WIDTH;
global PATCHES_HEIGHT;
sub_patches = cell(PATCHES_HEIGHT, PATCHES_WIDTH);
for i = 1:PATCHES_HEIGHT
    for j = 1:PATCHES_WIDTH
        i_begin = PATCH_SIDE_X*(i-1)+1;
        i_end = PATCH_SIDE_X*i;
        j_begin = PATCH_SIDE_Y*(j-1)+1;
        j_end = PATCH_SIDE_Y*j;
        sub_patches{i,j} = double(I(i_begin:i_end, j_begin:j_end, 1:3));
    end
end
end
