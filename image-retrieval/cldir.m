function [] = cldir()
    I1 = imread('1.jpg');
    patches1 = image_split(I1);
    icons1 = image_icons(patches1);
    iconsmat1 = cell2mat(icons1);
    [Y1,Cb1,Cr1] = image_trans(iconsmat1);
    YCbCr1 = image_zigzag(Y1,Cb1,Cr1);
    
    I2 = imread('2.jpg');
    patches2 = image_split(I2);
    icons2 = image_icons(patches2);
    iconsmat2 = cell2mat(icons2);
    [Y2,Cb2,Cr2] = image_trans(iconsmat2);
    YCbCr2 = image_zigzag(Y2,Cb2,Cr2);
    P = image_match(YCbCr1, YCbCr2)
end

% Q:    YCbCr1
% D:    YCbCr2
%% 图像匹配，输入两个描述符，返回P值
function P = image_match(YCbCr1, YCbCr2)
    P = double(0);
    YCbCr = double(zeros(1,3));
    for i = 1:3
        for j = 1:10
            w = double(0);
            if YCbCr1(i,j) == 0 || YCbCr2(i,j) == 0
                w = 1;
            else
                w = YCbCr1(i,j);
            end
            YCbCr(i) = YCbCr(i) + w * ((YCbCr1(i,j)-YCbCr2(i,j)) ^ 2);
        end
    end
    P = sqrt(YCbCr(1)) + sqrt(YCbCr(2)) + sqrt(YCbCr(3));
end


%% 对一个8*8的YCbCr空间上的三个分量进行Z字形扫描
function YCbCr = image_zigzag(Y,Cb,Cr)
    YCbCr = double(zeros(0));
    YCbCr = [YCbCr; zigzag(Y)];
    YCbCr = [YCbCr; zigzag(Cb)];
    YCbCr = [YCbCr; zigzag(Cr)];
end


%% 对YCbCr的一个分量进行Z字形扫描
function V = zigzag(M)
    V = double(zeros(1,10));
    V(1) = M(1,1);
    V(2) = M(1,2);
    V(3) = M(2,1);
    V(4) = M(3,1);
    V(5) = M(2,2);
    V(6) = M(1,3);
    V(7) = M(1,4);
    V(8) = M(2,3);
    V(9) = M(3,2);
    V(10) = M(4,1);
end


%% 图像颜色空间转换，从RGB到YCbCr
function [Y,Cb,Cr] = image_trans(iconsmat)
    YCbCr = double(zeros(8,8,3));
    for i = 1:8
        for j = 1:8
            RGB = iconsmat(i,j,1:3);
            YCbCr(i,j,1) = 0.299*RGB(1) + 0.587*RGB(2) + 0.114*RGB(3);
            YCbCr(i,j,2) = -0.169*RGB(1) - 0.331*RGB(2) + 0.5*RGB(3);
            YCbCr(i,j,3) = 0.5*RGB(1) - 0.419*RGB(2) - 0.081*RGB(3);
        end
    end
    Y = dct2(YCbCr(:,:,1));
    Cb = dct2(YCbCr(:,:,2));
    Cr = dct2(YCbCr(:,:,3));
end


%% 计算每个块的代表颜色
function [RGB] = image_icon(patch)
    size_t = size(patch);
    size_height = size_t(1);
    size_width = size_t(2);
    patch = double(patch);
    RGB = double(zeros(1,1,3));
    for i = 1:size_height
        for j = 1:size_width
            for k = 1:3
                RGB(1,1,k) = RGB(1,1,k) + patch(i,j,k);
            end
        end
    end
    RGB = uint8(RGB / (size_height * size_width));
end


%% 计算一个8*8的块组成的图像的代表颜色
function [icons] = image_icons(patches)
    icons = cell(8,8);
    for i = 1:8
        for j = 1:8
            icon = image_icon(patches{i,j});
            icons{i,j} = icon;
        end
    end
end


%% 图像分割，将输入的图像分割成8*8大小的块
function [patches] = image_split(image)
    size_t = size(image);
    size_height = size_t(1);
    size_width = size_t(2);
    patch_height = size_height / 8;
    patch_width = size_width / 8;
    patches = cell(8,8);
    for i = 1:8
        for j = 1:8
            i_begin = patch_height * (i-1) + 1;
            i_end = patch_height * i;
            j_begin = patch_width * (j-1) + 1;
            j_end = patch_width * j;
            x = image(i_begin:i_end, j_begin:j_end, 1:3);
            patches{i,j} = x;
        end
    end
end